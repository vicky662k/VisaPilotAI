from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.services.matching_service import create_job_match


router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.post("/resume/{resume_id}")
def match_resume(
    resume_id: int,
):
    db: Session = SessionLocal()

    try:
        # Get resume
        resume = (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found",
            )

        # Get all jobs
        jobs = (
            db.query(Job)
            .order_by(Job.id)
            .all()
        )

        matches = []

        for job in jobs:

            match = create_job_match(
                db=db,
                user_id=resume.user_id,
                resume=resume,
                job=job,
            )

            matches.append(
                {
                    "job_id": job.id,
                    "company": job.company,
                    "title": job.title,
                    "location": job.location,
                    "job_url": job.job_url,
                    "source": job.source,
                    "match_score": match.match_score,
                    "skill_match_score": match.skill_match_score,
                    "location_score": match.location_match,
                    "visa_match": match.visa_match,
                    "relocation_support": job.relocation_support,
                }
            )

        # Visa-sponsored jobs first,
        # then highest match score.
        matches.sort(
            key=lambda x: (
                bool(x["visa_match"]),
                x["match_score"] or 0,
            ),
            reverse=True,
        )

        return {
            "resume_id": resume_id,
            "total_jobs": len(jobs),
            "matches": matches,
        }

    finally:
        db.close()