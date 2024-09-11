from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.models.base import Base


class File(Base):
    __tablename__ = 'file'

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_filename: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    path: Mapped[str]
    filename: Mapped[str]
    size: Mapped[int]
    content_type: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='files')
