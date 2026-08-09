from unittest.mock import patch

from app.database.database import SessionLocal
from app.models.job import Job

from app.services.greenhouse_service import (
    update_existing_greenhouse_jobs,
)


db = SessionLocal()

try:
    # Job ID 3 will be our simulated stale job.
    stale_job = (
        db.query(Job)
        .filter(Job.id == 3)
        .first()
    )

    if not stale_job:
        print("Job ID 3 not found.")
        raise SystemExit

    # Make sure the job starts as active.
    stale_job.is_active = True
    db.commit()

    print(
        f"Before test: "
        f"ID={stale_job.id} | "
        f"Title={stale_job.title} | "
        f"Active={stale_job.is_active}"
    )

    # Build a fake Greenhouse response.
    #
    # Important:
    # Job ID 3 is intentionally NOT included.
    # This simulates Greenhouse no longer returning
    # this job.
    fake_greenhouse_jobs = []

    active_jobs = (
        db.query(Job)
        .filter(
            Job.source == "greenhouse",
            Job.is_active == True,
            Job.id != stale_job.id,
        )
        .all()
    )

    for job in active_jobs:

        fake_greenhouse_jobs.append(
            {
                "absolute_url": job.job_url,
                "title": job.title,
                "location": {
                    "name": job.location,
                },
                "content": job.description or "",
            }
        )

    print(
        "Simulated Greenhouse jobs:",
        len(fake_greenhouse_jobs),
    )

    with patch(
        "app.services.greenhouse_service.fetch_greenhouse_jobs",
        return_value=fake_greenhouse_jobs,
    ):

        result = update_existing_greenhouse_jobs(
            db=db,
            board_token="greenhouse",
        )

    db.refresh(stale_job)

    print(
        f"After discovery: "
        f"ID={stale_job.id} | "
        f"Active={stale_job.is_active}"
    )

    print(
        "Updated:",
        result["updated"],
    )

    print(
        "Deactivated:",
        result["deactivated"],
    )

    if stale_job.is_active is False:
        print(
            "\nPASS: stale job was "
            "automatically deactivated."
        )
    else:
        print(
            "\nFAIL: stale job remained active."
        )

finally:
    db.close()