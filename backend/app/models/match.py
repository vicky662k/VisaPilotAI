from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.sql import func

from app.database.base import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

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

    match_score = Column(
        Float,
        nullable=False,
        default=0,
    )

    skill_match_score = Column(
        Float,
        nullable=False,
        default=0,
    )

    location_match = Column(
    Float,
    nullable=False,
    default=0.0,
    )

    visa_match = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )