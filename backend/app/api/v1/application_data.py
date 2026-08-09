from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.application_data_service import (
    get_application_data,
)


router = APIRouter(
    prefix="/application-data",
    tags=["Application Data"],
)


@router.get("/{application_id}")
def get_application_application_data(
    application_id: int,
    db: Session = Depends(get_db),
):
    data = get_application_data(
        db=db,
        application_id=application_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    # Do not expose full resume extracted text
    # through this endpoint.
    data["resume"].pop(
        "extracted_text",
        None,
    )

    return data