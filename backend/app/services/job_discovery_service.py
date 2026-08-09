from sqlalchemy.orm import Session

from app.core.job_sources import JOB_SOURCES

from app.models.resume import Resume

from app.services.greenhouse_service import (
    save_greenhouse_jobs,
    update_existing_greenhouse_jobs,
)

from app.services.matching_service import (
    match_active_jobs_for_resume,
)


def discover_jobs(
    db: Session,
    resume_id: int | None = None,
):
    total_found = 0
    total_saved = 0
    total_updated = 0
    total_deactivated = 0
    total_matched = 0

    results = []

    # --------------------------------------------------
    # Get resume for automatic matching
    # --------------------------------------------------

    resume = None

    if resume_id is not None:

        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
        )

        if resume is None:
            raise ValueError(
                f"Resume {resume_id} not found"
            )

    # --------------------------------------------------
    # Greenhouse discovery
    # --------------------------------------------------

    greenhouse_config = JOB_SOURCES.get(
        "greenhouse",
        {},
    )

    if greenhouse_config.get("enabled"):

        for board_token in greenhouse_config.get(
            "boards",
            [],
        ):

            save_result = save_greenhouse_jobs(
                db=db,
                board_token=board_token,
            )

            update_result = (
                update_existing_greenhouse_jobs(
                    db=db,
                    board_token=board_token,
                )
            )

            total_found += (
                save_result["total_found"]
            )

            total_saved += (
                save_result["saved"]
            )

            total_updated += (
                update_result["updated"]
            )

            total_deactivated += (
                update_result.get(
                    "deactivated",
                    0,
                )
            )

            results.append(
                {
                    "source": "greenhouse",
                    "board_token": board_token,
                    "found": save_result[
                        "total_found"
                    ],
                    "saved": save_result[
                        "saved"
                    ],
                    "updated": update_result[
                        "updated"
                    ],
                    "deactivated": update_result.get(
                        "deactivated",
                        0,
                    ),
                }
            )

    # --------------------------------------------------
    # M6.5 — Automatic matching
    # --------------------------------------------------

    if resume is not None:

        matches = match_active_jobs_for_resume(
            db=db,
            user_id=resume.user_id,
            resume=resume,
        )

        total_matched = len(matches)

    # --------------------------------------------------
    # Return discovery + matching result
    # --------------------------------------------------

    return {
        "resume_id": resume_id,
        "total_found": total_found,
        "total_saved": total_saved,
        "total_updated": total_updated,
        "total_deactivated": total_deactivated,
        "total_matched": total_matched,
        "sources": results,
    }