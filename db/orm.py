import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)

    uploads: Mapped[List['Upload']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Upload(Base):
    __tablename__ = 'uploads'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(default=str(uuid.uuid4()), nullable=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    upload_time: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    finish_time: Mapped[datetime] = mapped_column(default=None, nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='uploads')

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'

    def upload_path(self) -> str:

        return f"C:/Users/Adiel/Desktop/Excellent/final-project-AdielDror/uploads/{self.filename}"

    @property
    def error_messages(self):

        return "Error messages for failed upload"
