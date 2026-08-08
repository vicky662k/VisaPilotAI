from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import (
    create_job,
    get_job_by_id,
    get_jobs,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/", response_model=JobResponse)
def add_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return create_job(db, job)


@router.get("/", response_model=list[JobResponse])
def list_jobs(
    db: Session = Depends(get_db),
):
    return get_jobs(db)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job