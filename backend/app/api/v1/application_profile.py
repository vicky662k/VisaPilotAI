from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.application_profile import (
    ApplicationProfileCreate,
    ApplicationProfileResponse,
    ApplicationProfileUpdate,
)
from app.services.application_profile_service import (
    create_application_profile,
    get_application_profile,
    update_application_profile,
)


router = APIRouter(
    prefix="/application-profile",
    tags=["Application Profile"],
)


@router.post(
    "/{user_id}",
    response_model=ApplicationProfileResponse,
)
def create_profile(
    user_id: int,
    profile: ApplicationProfileCreate,
    db: Session = Depends(get_db),
):
    existing_profile = get_application_profile(
        db=db,
        user_id=user_id,
    )

    if existing_profile:
        raise HTTPException(
            status_code=409,
            detail="Application profile already exists",
        )

    return create_application_profile(
        db=db,
        user_id=user_id,
        profile=profile,
    )


@router.get(
    "/{user_id}",
    response_model=ApplicationProfileResponse,
)
def get_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    profile = get_application_profile(
        db=db,
        user_id=user_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Application profile not found",
        )

    return profile


@router.put(
    "/{user_id}",
    response_model=ApplicationProfileResponse,
)
def update_profile(
    user_id: int,
    profile: ApplicationProfileUpdate,
    db: Session = Depends(get_db),
):
    updated_profile = update_application_profile(
        db=db,
        user_id=user_id,
        profile=profile,
    )

    if not updated_profile:
        raise HTTPException(
            status_code=404,
            detail="Application profile not found",
        )

    return updated_profile