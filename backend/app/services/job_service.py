from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate


def create_job(db: Session, job: JobCreate):

    db_job = Job(
        company=job.company,
        title=job.title,
        location=job.location,
        description=job.description,
        job_url=job.job_url,
        source=job.source,
        visa_sponsorship=job.visa_sponsorship,
        relocation_support=job.relocation_support,
    )

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


def get_jobs(db: Session):

    return db.query(Job).order_by(
        Job.created_at.desc()
    ).all()


def get_job_by_id(db: Session, job_id: int):

    return (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )
