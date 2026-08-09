from datetime import datetime

from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
)


VALID_STATUSES = {
    "saved",
    "prepared",
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn",
}


def get_application(
    db: Session,
    application_id: int,
):
    return (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )


def get_user_applications(
    db: Session,
    user_id: int,
):
    return (
        db.query(Application)
        .filter(
            Application.user_id == user_id
        )
        .order_by(
            Application.created_at.desc()
        )
        .all()
    )


def create_application(
    db: Session,
    application: ApplicationCreate,
):
    if application.status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid application status: "
            f"{application.status}"
        )

    existing_application = (
        db.query(Application)
        .filter(
            Application.user_id
            == application.user_id,
            Application.job_id
            == application.job_id,
        )
        .first()
    )

    if existing_application:
        return existing_application

    db_application = Application(
        user_id=application.user_id,
        job_id=application.job_id,
        resume_id=application.resume_id,
        status=application.status,
        application_url=application.application_url,
        notes=application.notes,
    )

    if application.status == "applied":
        db_application.applied_at = datetime.utcnow()

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


def update_application(
    db: Session,
    application_id: int,
    application: ApplicationUpdate,
):
    db_application = get_application(
        db=db,
        application_id=application_id,
    )

    if not db_application:
        return None

    update_data = application.model_dump(
        exclude_unset=True
    )

    if "status" in update_data:
        status = update_data["status"]

        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid application status: "
                f"{status}"
            )

        if (
            status == "applied"
            and db_application.applied_at is None
        ):
            db_application.applied_at = datetime.utcnow()

    for field, value in update_data.items():
        setattr(
            db_application,
            field,
            value,
        )

    db.commit()
    db.refresh(db_application)

    return db_application