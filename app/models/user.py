import re

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates,
)

from app.models.base import Base
from config import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(MAX_USERNAME_LENGTH), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(MAX_EMAIL_LENGTH),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(nullable=False)

    files = relationship(
        'File', back_populates='user', cascade='all, delete-orphan'
    )

    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError('Неправильный формат почты')
        return email

    @validates('username')
    def validate_first_name(self, key, username):
        username_regex = r'^[\w.@+-]+$'
        if not re.match(username_regex, username):
            raise ValueError('Недопустимые символы в имени')
        return username
