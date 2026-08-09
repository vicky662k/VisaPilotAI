from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApplicationProfileCreate(BaseModel):
    phone: Optional[str] = None

    address_line1: Optional[str] = None
    address_line2: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None

    current_title: Optional[str] = None
    work_authorization: Optional[str] = None

    requires_visa_sponsorship: bool = True
    willing_to_relocate: bool = True


class ApplicationProfileUpdate(BaseModel):
    phone: Optional[str] = None

    address_line1: Optional[str] = None
    address_line2: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None

    current_title: Optional[str] = None
    work_authorization: Optional[str] = None

    requires_visa_sponsorship: Optional[bool] = None
    willing_to_relocate: Optional[bool] = None


class ApplicationProfileResponse(ApplicationProfileCreate):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True