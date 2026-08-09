import requests

from sqlalchemy.orm import Session

from app.models.job import Job

from app.services.job_normalizer import (
    normalize_job_data,
)

from app.services.visa_detector import (
    detect_visa_sponsorship,
    detect_relocation_support,
)


GREENHOUSE_URL = (
    "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
)


def fetch_greenhouse_jobs(
    board_token: str,
):
    url = GREENHOUSE_URL.format(
        board_token=board_token
    )

    response = requests.get(
        url,
        params={"content": "true"},
        timeout=30,
    )

    response.raise_for_status()

    return response.json().get(
        "jobs",
        []
    )


def save_greenhouse_jobs(
    db: Session,
    board_token: str,
):
    jobs = fetch_greenhouse_jobs(
        board_token
    )

    saved_jobs = 0

    for job in jobs:

        job_url = job.get(
            "absolute_url"
        )

        if not job_url:
            continue

        existing_job = (
            db.query(Job)
            .filter(
                Job.job_url == job_url
            )
            .first()
        )

        if existing_job:
            continue

        location = (
            job.get(
                "location",
                {}
            ).get("name")
        )

        description = (
            job.get("content")
            or ""
        )

        normalized = normalize_job_data(
            company=board_token,
            title=job.get("title"),
            location=location,
            description=description,
            job_url=job_url,
            source="greenhouse",
        )

        visa_sponsorship = (
            detect_visa_sponsorship(
                normalized["description"]
            )
        )

        relocation_support = (
            detect_relocation_support(
                normalized["description"]
            )
        )

        new_job = Job(
            company=normalized["company"],
            title=normalized["title"],
            location=normalized["location"],
            description=normalized["description"],
            job_url=normalized["job_url"],
            source=normalized["source"],
            visa_sponsorship=visa_sponsorship,
            relocation_support=relocation_support,
            is_active=True,
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
    jobs = fetch_greenhouse_jobs(
        board_token
    )

    updated_jobs = 0
    deactivated_jobs = 0

    # Collect all job URLs currently returned
    # by Greenhouse.
    current_job_urls = {
        job.get("absolute_url")
        for job in jobs
        if job.get("absolute_url")
    }

    # Update jobs that still exist in the
    # current Greenhouse feed.
    for job in jobs:

        job_url = job.get(
            "absolute_url"
        )

        if not job_url:
            continue

        existing_job = (
            db.query(Job)
            .filter(
                Job.job_url == job_url
            )
            .first()
        )

        if existing_job is None:
            continue

        existing_job.is_active = True

        location = (
            job.get(
                "location",
                {}
            ).get("name")
        )

        description = (
            job.get("content")
            or ""
        )

        normalized = normalize_job_data(
            company=board_token,
            title=job.get("title"),
            location=location,
            description=description,
            job_url=job_url,
            source="greenhouse",
        )

        existing_job.company = (
            normalized["company"]
        )

        existing_job.title = (
            normalized["title"]
        )

        existing_job.location = (
            normalized["location"]
        )

        existing_job.description = (
            normalized["description"]
        )

        existing_job.job_url = (
            normalized["job_url"]
        )

        existing_job.source = (
            normalized["source"]
        )

        existing_job.visa_sponsorship = (
            detect_visa_sponsorship(
                normalized["description"]
            )
        )

        existing_job.relocation_support = (
            detect_relocation_support(
                normalized["description"]
            )
        )

        updated_jobs += 1

    # Find existing jobs belonging to this
    # Greenhouse source.
    existing_greenhouse_jobs = (
        db.query(Job)
        .filter(
            Job.source == "greenhouse",
            Job.company == board_token,
            Job.is_active == True,
        )
        .all()
    )

    # Jobs that existed previously but are no
    # longer returned by Greenhouse are stale.
    for existing_job in existing_greenhouse_jobs:

        if existing_job.job_url not in current_job_urls:

            existing_job.is_active = False

            deactivated_jobs += 1

    db.commit()

    return {
        "total_found": len(jobs),
        "updated": updated_jobs,
        "deactivated": deactivated_jobs,
    }