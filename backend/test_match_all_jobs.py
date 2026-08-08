from app.database.database import SessionLocal
from app.models.resume import Resume
from app.services.matching_service import (
    match_resume_to_all_jobs,
)


db = SessionLocal()

try:

    resume = (
        db.query(Resume)
        .filter(Resume.id == 1)
        .first()
    )

    if resume is None:
        print("Resume not found")
        raise SystemExit

    matches = match_resume_to_all_jobs(
        db=db,
        user_id=resume.user_id,
        resume=resume,
    )

    print("\n===== ALL JOB MATCHES =====")

    for match in matches:

        print(
            f"Job ID: {match.job_id} | "
            f"Match: {match.match_score}% | "
            f"Skills: {match.skill_match_score}% | "
            f"Location: {match.location_match} | "
            f"Visa: {match.visa_match}"
        )

    print("\nTotal jobs matched:", len(matches))

finally:
    db.close()