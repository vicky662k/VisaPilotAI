from sqlalchemy.orm import Session

from app.models.application_profile import ApplicationProfile
from app.schemas.application_profile import (
    ApplicationProfileCreate,
    ApplicationProfileUpdate,
)


def get_application_profile(
    db: Session,
    user_id: int,
):
    return (
        db.query(ApplicationProfile)
        .filter(
            ApplicationProfile.user_id == user_id
        )
        .first()
    )


def create_application_profile(
    db: Session,
    user_id: int,
    profile: ApplicationProfileCreate,
):
    existing_profile = get_application_profile(
        db=db,
        user_id=user_id,
    )

    if existing_profile:
        return existing_profile

    db_profile = ApplicationProfile(
        user_id=user_id,
        **profile.model_dump(),
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


def update_application_profile(
    db: Session,
    user_id: int,
    profile: ApplicationProfileUpdate,
):
    db_profile = get_application_profile(
        db=db,
        user_id=user_id,
    )

    if not db_profile:
        return None

    update_data = profile.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            db_profile,
            field,
            value,
        )

    db.commit()
    db.refresh(db_profile)

    return db_profile