import re

from fastapi.exceptions import ValidationException
from pydantic import BaseModel, EmailStr, Field, field_validator

from config import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH


class UserAuthentication(BaseModel):
    email: EmailStr = Field(max_length=MAX_EMAIL_LENGTH)
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        password_regex = re.compile(
            r'^'
            r'(?=.*[a-z])'
            r'(?=.*[A-Z])'
            r'(?=.*\d)'
            r'(?=.*[@$!%*?&])'
            r'[A-Za-z\d@$!%*?&]'
            r'{8,}$'
        )
        if not password_regex.match(value):
            raise ValidationException(
                'Длина пароля не менее 8 символов, включая '
                'строчные, прописные буквы, числа, '
                'и специальные символы.'
            )
        return value


class UserCreate(UserAuthentication):
    username: str = Field(max_length=MAX_USERNAME_LENGTH, pattern=r'^[\w.@+-]+$')


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
