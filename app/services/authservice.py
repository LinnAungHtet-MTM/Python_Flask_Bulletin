from datetime import datetime, timedelta
from app.dao.password_reset_dao import PasswordResetDao
from app.exceptions.business_exception import BusinessException
from app.extension import db
from app.templates.mails.mailservice import send_reset_password_email
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, decode_token, create_refresh_token
from app.dao.userdao import UserDao
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()


class AuthService:

    # Login
    @staticmethod
    def login(payload):
        user = UserDao.find_by_email(payload.email)

        if not user:
            raise BusinessException(
                field="email",
                message="Selected Email Address doesn't exist"
            )

        if not check_password_hash(user.password, payload.password):
            raise BusinessException(
                field="password",
                message="Invalid credentials"
            )

        if user.lock_flg:
            raise BusinessException(
                field="password",
                message="Your Account has been locked"
            )

        # update last login
        user.last_login_at = datetime.utcnow()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            })

        refresh_expires = (
            timedelta(days=30)
            if payload.remember
            else timedelta(hours=12)
        )

        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=refresh_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "refresh_expires": refresh_expires
        }


    # Generate Refresh Token
    @staticmethod
    def refresh_token(user_id: int):
        # Check if user exists
        user = UserDao.find_by_id(user_id)
        if not user:
            return {
                "success": False,
                "message": "User not found"
            }

        # Create new access token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )

        return {
            "success": True,
            "data": {
                "access_token": access_token
            }
        }


    # Forgot Password
    @staticmethod
    def forgot_password(payload):
        user = UserDao.find_by_email(payload.email)
        if not user:
            raise BusinessException(
                field="email",
                message="Selected Email Address doesn't exist"
            )

        token = AuthService.generate_reset_token(payload.email)
        token_hash = AuthService.hash_token(token)
        FRONTEND_URL = os.getenv("FRONTEND_URL")
        PasswordResetDao.create(payload.email, token_hash)

        reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

        send_reset_password_email(payload.email, reset_link)


    # Reset Token
    @staticmethod
    def generate_reset_token(email: str):
        token = create_access_token(
            identity=email,
            expires_delta=timedelta(minutes=10),
            additional_claims={"type": "reset"}
        )
        return token


    # Verify Reset Token
    @staticmethod
    def verify_reset_token(token: str):
        if not token:
            return {
                "field": "token",
                "success": False,
                "message": "Token required"
            }

        try:
            decoded = decode_token(token)
        except Exception:
            return {
                "field": "token",
                "success": False,
                "message": "Invalid or Expire token"
            }

        if decoded.get("type") != "reset":
            return {
                "field": "token",
                "success": False,
                "message": "Invalid token"
            }

        token_hash = AuthService.hash_token(token)

        reset = PasswordResetDao.find_valid(
            email=decoded["sub"],
            token_hash=token_hash
        )

        if not reset:
            return {
                "field": "token",
                "success": False,
                "message": "Invalid token or already used"
            }

        return {
            "success": True,
        }


    # Reset Password
    @staticmethod
    def reset_password(payload):
        try:
            decoded = decode_token(payload.token)
        except Exception:
            raise BusinessException(
                field="token",
                message="Invalid or expired token"
            )

        if decoded.get("type") != "reset":
            raise BusinessException(
                field="token",
                message="Invalid token"
            )

        token_hash = AuthService.hash_token(payload.token)

        reset = PasswordResetDao.find_valid(
            email=decoded["sub"],
            token_hash=token_hash
        )

        if not reset:
            raise BusinessException(
                field="token",
                message="Token already used or invalid"
            )

        # Check User Exist
        user = UserDao.find_by_email(decoded["sub"])
        if not user:
            raise BusinessException(
                field="email",
                message="User not found"
            )

        # Update Password
        user.password = generate_password_hash(payload.password)

        # Invalidate token
        reset.deleted_at = datetime.utcnow()


    # Token Hash
    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
