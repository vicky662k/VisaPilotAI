import requests
from sqlalchemy.orm import Session

from app.models.job import Job


GREENHOUSE_URL = (
    "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
)


def fetch_greenhouse_jobs(board_token: str):
    url = GREENHOUSE_URL.format(
        board_token=board_token
    )

    response = requests.get(
        url,
        params={"content": "true"},
        timeout=30,
    )

    response.raise_for_status()

    return response.json().get("jobs", [])


def save_greenhouse_jobs(
    db: Session,
    board_token: str,
):

    jobs = fetch_greenhouse_jobs(board_token)

    saved_jobs = 0

    for job in jobs:

        job_url = job.get("absolute_url")

        if not job_url:
            continue

        existing_job = (
            db.query(Job)
            .filter(Job.job_url == job_url)
            .first()
        )

        if existing_job:
            continue

        location = (
            job.get("location", {})
            .get("name")
        )

        new_job = Job(
            company=board_token,
            title=job.get("title", ""),
            location=location,
            description=job.get("content"),
            job_url=job_url,
            source="greenhouse",
            visa_sponsorship=False,
            relocation_support=False,
        )

        db.add(new_job)
        saved_jobs += 1

    db.commit()

    return {
        "total_found": len(jobs),
        "saved": saved_jobs,
    }