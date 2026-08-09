from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class ApplicationProfile(Base):
    __tablename__ = "application_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    phone = Column(
        String(50),
        nullable=True,
    )

    address_line1 = Column(
        String(255),
        nullable=True,
    )

    address_line2 = Column(
        String(255),
        nullable=True,
    )

    city = Column(
        String(100),
        nullable=True,
    )

    state = Column(
        String(100),
        nullable=True,
    )

    postal_code = Column(
        String(20),
        nullable=True,
    )

    country = Column(
        String(100),
        nullable=True,
    )

    linkedin_url = Column(
        String(500),
        nullable=True,
    )

    github_url = Column(
        String(500),
        nullable=True,
    )

    portfolio_url = Column(
        String(500),
        nullable=True,
    )

    current_title = Column(
        String(255),
        nullable=True,
    )

    work_authorization = Column(
        String(255),
        nullable=True,
    )

    requires_visa_sponsorship = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    willing_to_relocate = Column(
        Boolean,
        default=True,
        nullable=False,
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

    user = relationship(
        "User",
    )