from sqlalchemy import or_
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

    return (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .all()
    )


def get_job_by_id(
    db: Session,
    job_id: int,
):

    return (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )


def search_jobs(
    db: Session,
    keyword: str | None = None,
    location: str | None = None,
    visa_sponsorship: bool | None = None,
    relocation_support: bool | None = None,
    source: str | None = None,
):

    query = db.query(Job)

    if keyword:
        search_term = f"%{keyword}%"

        query = query.filter(
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term),
                Job.description.ilike(search_term),
            )
        )

    if location:
        query = query.filter(
            Job.location.ilike(
                f"%{location}%"
            )
        )

    if visa_sponsorship is not None:
        query = query.filter(
            Job.visa_sponsorship == visa_sponsorship
        )

    if relocation_support is not None:
        query = query.filter(
            Job.relocation_support == relocation_support
        )

    if source:
        query = query.filter(
            Job.source.ilike(
                f"%{source}%"
            )
        )

    return (
        query
        .order_by(Job.created_at.desc())
        .all()
    )