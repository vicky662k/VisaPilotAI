from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int
    resume_id: int

    status: str = "saved"

    application_url: Optional[str] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    application_url: Optional[str] = None
    notes: Optional[str] = None
    applied_at: Optional[datetime] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_id: int

    status: str

    application_url: Optional[str] = None
    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True