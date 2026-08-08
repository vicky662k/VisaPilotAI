from app.database.database import SessionLocal
from app.models.resume import Resume
from app.models.job import Job

from app.services.matching_service import (
    extract_experience_requirement,
    extract_resume_experience,
)


db = SessionLocal()

try:
    resume = (
        db.query(Resume)
        .filter(Resume.id == 1)
        .first()
    )

    job = (
        db.query(Job)
        .filter(Job.id == 1)
        .first()
    )

    if resume is None:
        print("Resume not found")
        raise SystemExit

    if job is None:
        print("Job not found")
        raise SystemExit

    resume_experience = extract_resume_experience(
        resume.extracted_text or ""
    )

    job_requirement = extract_experience_requirement(
        job.description or ""
    )

    print("\n===== EXPERIENCE TEST =====")
    print("Candidate experience:", resume_experience)
    print("Job required experience:", job_requirement)

finally:
    db.close()