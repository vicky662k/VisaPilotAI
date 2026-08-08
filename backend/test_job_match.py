from app.database.database import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.services.matching_service import (
    create_job_match,
    get_skill_match_details,
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

    details = get_skill_match_details(
        resume.extracted_text or "",
        job.description or "",
    )

    match = create_job_match(
        db=db,
        user_id=resume.user_id,
        resume=resume,
        job=job,
    )

    print("\n===== JOB MATCH =====")
    print("Match ID:", match.id)
    print("Job:", job.title)
    print("Location:", job.location)

    print("\nMatched skills:")
    for skill in details["matched_skills"]:
        print("✓", skill)

    print("\nMissing skills:")
    for skill in details["missing_skills"]:
        print("✗", skill)

    print("\nSkill Match:", details["skill_score"])
    print("Location Match:", match.location_match)
    print("Visa Match:", match.visa_match)
    print("Overall Match:", match.match_score)

finally:
    db.close()