import re
from pydantic_core import PydanticCustomError

PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,20}$"


# Password Validate Format
def validate_password_format(v: str) -> str:
    if not re.match(PASSWORD_PATTERN, v):
        raise PydanticCustomError(
            "password_invalid",
            "Password must be 6–20 characters and include at least "
            "one uppercase, lowercase letter & one digit"
        )
    return v


# Password & Confirm Password Match
def passwords_match(cls, v, info):
    password = info.data.get("password")

    if not password:
        return v
    if v != password:
        raise PydanticCustomError(
            "password_mismatch",
            "Confirm Password and Password must match"
        )
    return v


# Email Validate Length
def validate_email_format(cls, v):
    if len(v) > 50:
        raise PydanticCustomError(
            "email_too_long",
            "Email must not be greater than 50 characters"
        )
    return v


# Title Validate Length
def validate_title_format(cls, v):
    if len(v) > 255:
        raise PydanticCustomError(
            "title_too_long",
            "title field must not be greater than 255"
        )
    return v
