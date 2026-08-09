from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    company = Column(
        String(255),
        nullable=False,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    location = Column(
        String(255),
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    job_url = Column(
        String(1000),
        unique=True,
        nullable=True,
    )

    source = Column(
        String(100),
        nullable=True,
    )

    visa_sponsorship = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    relocation_support = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )