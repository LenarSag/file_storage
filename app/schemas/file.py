from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class FileBase(BaseModel):
    unique_filename: UUID
    filename: str
    size: int
    content_type: str


class FileToDB(FileBase):
    path: str
    user_id: int


class FileDB(FileBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
