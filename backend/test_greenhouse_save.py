from app.database.database import SessionLocal
from app.services.greenhouse_service import save_greenhouse_jobs


db = SessionLocal()

try:
    result = save_greenhouse_jobs(
        db=db,
        board_token="greenhouse",
    )

    print("Greenhouse import complete!")
    print("Total jobs found:", result["total_found"])
    print("New jobs saved:", result["saved"])

finally:
    db.close()