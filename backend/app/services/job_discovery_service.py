from sqlalchemy.orm import Session

from app.core.job_sources import JOB_SOURCES

from app.services.greenhouse_service import (
    save_greenhouse_jobs,
    update_existing_greenhouse_jobs,
)


def discover_jobs(
    db: Session,
):
    total_found = 0
    total_saved = 0
    total_updated = 0
    total_deactivated = 0

    results = []

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

    return {
        "total_found": total_found,
        "total_saved": total_saved,
        "total_updated": total_updated,
        "total_deactivated": total_deactivated,
        "sources": results,
    }