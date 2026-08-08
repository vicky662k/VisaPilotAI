from pydantic import BaseModel
from typing import Optional


class JobCreate(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    description: Optional[str] = None
    job_url: Optional[str] = None
    source: Optional[str] = None
    visa_sponsorship: bool = False
    relocation_support: bool = False


class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True