from typing import Optional
from app.exceptions.field_validator import validate_title_format
from pydantic import BaseModel, field_validator

class CreatePostRequest(BaseModel):
    title: str
    description: str

    # Title length
    @field_validator("title")
    @classmethod
    def validate_title_length(cls, v):
        return validate_title_format(cls, v)


class PostSearchRequest(BaseModel):
    # keyword: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    date: Optional[str] = None


class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    # Title length
    @field_validator("title")
    @classmethod
    def validate_title_length(cls, v):
        return validate_title_format(cls, v)
