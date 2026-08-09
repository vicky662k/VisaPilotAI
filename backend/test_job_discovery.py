from app.database.database import SessionLocal

from app.services.job_discovery_service import (
    discover_jobs,
)


db = SessionLocal()

try:

    result = discover_jobs(
        db=db
    )

    print("\n===== M6.4 JOB DISCOVERY =====")

    print(
        "Total found:",
        result["total_found"],
    )

    print(
        "Total saved:",
        result["total_saved"],
    )

    print(
        "Total updated:",
        result["total_updated"],
    )

    print(
        "Total deactivated:",
        result.get(
            "total_deactivated",
            0,
        ),
    )

    print("\nSources:")

    for source in result["sources"]:

        print(
            f"{source['source']} | "
            f"{source['board_token']} | "
            f"Found: {source['found']} | "
            f"Saved: {source['saved']} | "
            f"Updated: {source['updated']} | "
            f"Deactivated: "
            f"{source.get('deactivated', 0)}"
        )

finally:

    db.close()