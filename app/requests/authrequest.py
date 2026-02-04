import re
from app.exceptions.field_validator import passwords_match, validate_email_format, validate_password_format
from pydantic import BaseModel, EmailStr, field_validator

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember: bool

    # Email length
    @field_validator("email")
    @classmethod
    def validate_email_length(cls, v):
        return validate_email_format(cls, v)

    # Password format
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_format(v)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetTokenRequest(BaseModel):
    token: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str
    confirm_password: str

    # Password format
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_format(v)

    # Password Match
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        return passwords_match(cls, v, info)
