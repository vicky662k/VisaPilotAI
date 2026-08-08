from app.database.database import SessionLocal
from app.services.greenhouse_service import (
    update_existing_greenhouse_jobs,
)


db = SessionLocal()

try:
    result = update_existing_greenhouse_jobs(
        db=db,
        board_token="greenhouse",
    )

    print("Greenhouse sponsorship detection complete!")
    print("Total jobs found:", result["total_found"])
    print("Jobs updated:", result["updated"])

finally:
    db.close()