import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    processing_status = Column(
        String,
        default="PENDING",
        nullable=False,
        index=True
    )

    upload_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    summary = Column(
        String,
        nullable=True
    )

    owner = relationship(
        "User",
        back_populates="documents"
    )

    embeddings = relationship(
        "DocumentEmbedding",
        back_populates="document",
        cascade="all, delete-orphan"
    )