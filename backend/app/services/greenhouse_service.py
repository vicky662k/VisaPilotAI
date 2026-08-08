import requests
from sqlalchemy.orm import Session

from app.models.job import Job
from app.services.visa_detector import (
    detect_visa_sponsorship,
    detect_relocation_support,
)


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

        description = job.get("content") or ""

        visa_sponsorship = detect_visa_sponsorship(
            description
        )

        relocation_support = detect_relocation_support(
            description
        )

        new_job = Job(
            company=board_token,
            title=job.get("title", ""),
            location=location,
            description=description,
            job_url=job_url,
            source="greenhouse",
            visa_sponsorship=visa_sponsorship,
            relocation_support=relocation_support,
        )

        db.add(new_job)

        saved_jobs += 1

    db.commit()

    return {
        "total_found": len(jobs),
        "saved": saved_jobs,
    }


def update_existing_greenhouse_jobs(
    db: Session,
    board_token: str,
):

    jobs = fetch_greenhouse_jobs(board_token)

    updated_jobs = 0

    for job in jobs:

        job_url = job.get("absolute_url")

        if not job_url:
            continue

        existing_job = (
            db.query(Job)
            .filter(Job.job_url == job_url)
            .first()
        )

        if existing_job is None:
            continue

        description = job.get("content") or ""

        existing_job.visa_sponsorship = (
            detect_visa_sponsorship(description)
        )

        existing_job.relocation_support = (
            detect_relocation_support(description)
        )

        updated_jobs += 1

    db.commit()

    return {
        "total_found": len(jobs),
        "updated": updated_jobs,
    }