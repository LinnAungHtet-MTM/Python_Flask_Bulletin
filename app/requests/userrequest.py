from typing import Optional, Literal
from app.exceptions.field_validator import passwords_match, validate_email_format, validate_password_format
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date

class UserSearchRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class LockUsersRequest(BaseModel):
    user_ids: list[int]
    lock_flg: Literal[0, 1]  # control allowed value


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: int
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

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

    # Password Match
    @field_validator("confirm_password", mode="after")
    @classmethod
    def passwords_match(cls, v, info):
        return passwords_match(cls, v, info)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[int] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

    # Email length
    @field_validator("email")
    @classmethod
    def validate_email_length(cls, v):
        return validate_email_format(cls, v)


class ChangePasswordRequest(BaseModel):
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
