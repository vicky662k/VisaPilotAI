from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.services.application_service import (
    create_application,
    get_application,
    get_user_applications,
    update_application,
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "/",
    response_model=ApplicationResponse,
)
def add_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_application(
            db=db,
            application=application,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/user/{user_id}",
    response_model=list[ApplicationResponse],
)
def list_user_applications(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_applications(
        db=db,
        user_id=user_id,
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application_by_id(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = get_application(
        db=db,
        application_id=application_id,
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def edit_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_application = update_application(
            db=db,
            application_id=application_id,
            application=application,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if not updated_application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return updated_application