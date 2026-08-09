from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.services.matching_service import (
    create_job_match,
    match_active_jobs_for_resume,
)


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
            .filter(
                Resume.id == resume_id
            )
            .first()
        )

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found",
            )

        # Get active jobs only
        jobs = (
            db.query(Job)
            .filter(
                Job.is_active == True
            )
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
                    "skill_match_score": (
                        match.skill_match_score
                    ),
                    "location_score": (
                        match.location_match
                    ),
                    "visa_match": match.visa_match,
                    "relocation_support": (
                        job.relocation_support
                    ),
                }
            )

        # Visa-sponsored jobs first,
        # then highest overall match score.
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


@router.get("/recommended/{resume_id}")
def get_recommended_jobs(
    resume_id: int,
    limit: int = 10,
    min_score: float = 50,
    visa_only: bool = False,
):
    db: Session = SessionLocal()

    try:
        # Validate limit
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="limit must be at least 1",
            )

        # Validate minimum score
        if min_score < 0 or min_score > 100:
            raise HTTPException(
                status_code=400,
                detail="min_score must be between 0 and 100",
            )

        # Get resume
        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
        )

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found",
            )

        # Get matches for active jobs only
        matches = match_active_jobs_for_resume(
            db=db,
            user_id=resume.user_id,
            resume=resume,
        )

        recommendations = []

        for match in matches:

            # Minimum match score filter
            if (
                match.match_score is None
                or match.match_score < min_score
            ):
                continue

            # Visa sponsorship filter
            if visa_only and not match.visa_match:
                continue

            # Get corresponding job
            job = (
                db.query(Job)
                .filter(
                    Job.id == match.job_id
                )
                .first()
            )

            if not job:
                continue

            recommendations.append(
                {
                    "job_id": job.id,
                    "company": job.company,
                    "title": job.title,
                    "location": job.location,
                    "job_url": job.job_url,
                    "source": job.source,
                    "match_score": match.match_score,
                    "skill_match_score": (
                        match.skill_match_score
                    ),
                    "location_score": (
                        match.location_match
                    ),
                    "visa_match": match.visa_match,
                    "relocation_support": (
                        job.relocation_support
                    ),
                }
            )

        # Visa-sponsored jobs first,
        # then highest overall match score.
        recommendations.sort(
            key=lambda x: (
                bool(x["visa_match"]),
                x["match_score"] or 0,
            ),
            reverse=True,
        )

        # Apply result limit
        recommendations = recommendations[:limit]

        return {
            "resume_id": resume_id,
            "total_recommendations": len(
                recommendations
            ),
            "limit": limit,
            "min_score": min_score,
            "visa_only": visa_only,
            "jobs": recommendations,
        }

    finally:
        db.close()