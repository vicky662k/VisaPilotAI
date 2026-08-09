from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False,
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="saved",
    )

    application_url = Column(
        String(1000),
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    applied_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )