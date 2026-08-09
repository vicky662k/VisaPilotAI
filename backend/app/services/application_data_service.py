from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.application_profile import ApplicationProfile
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User


def get_application_data(
    db: Session,
    application_id: int,
):
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if not application:
        return None

    user = (
        db.query(User)
        .filter(
            User.id == application.user_id
        )
        .first()
    )

    profile = (
        db.query(ApplicationProfile)
        .filter(
            ApplicationProfile.user_id
            == application.user_id
        )
        .first()
    )

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == application.resume_id
        )
        .first()
    )

    job = (
        db.query(Job)
        .filter(
            Job.id == application.job_id
        )
        .first()
    )

    return {
        "application": {
            "id": application.id,
            "status": application.status,
            "application_url": application.application_url,
            "notes": application.notes,
            "applied_at": application.applied_at,
        },
        "candidate": {
            "first_name": user.first_name if user else None,
            "last_name": user.last_name if user else None,
            "email": user.email if user else None,
            "country": user.country if user else None,
            "phone": profile.phone if profile else None,
            "address_line1": (
                profile.address_line1
                if profile
                else None
            ),
            "address_line2": (
                profile.address_line2
                if profile
                else None
            ),
            "city": profile.city if profile else None,
            "state": profile.state if profile else None,
            "postal_code": (
                profile.postal_code
                if profile
                else None
            ),
            "linkedin_url": (
                profile.linkedin_url
                if profile
                else None
            ),
            "github_url": (
                profile.github_url
                if profile
                else None
            ),
            "portfolio_url": (
                profile.portfolio_url
                if profile
                else None
            ),
            "current_title": (
                profile.current_title
                if profile
                else None
            ),
            "work_authorization": (
                profile.work_authorization
                if profile
                else None
            ),
            "requires_visa_sponsorship": (
                profile.requires_visa_sponsorship
                if profile
                else None
            ),
            "willing_to_relocate": (
                profile.willing_to_relocate
                if profile
                else None
            ),
        },
        "resume": {
            "id": resume.id if resume else None,
            "filename": (
                resume.filename
                if resume
                else None
            ),
            "extracted_text": (
                resume.extracted_text
                if resume
                else None
            ),
        },
        "job": {
            "id": job.id if job else None,
            "company": (
                job.company
                if job
                else None
            ),
            "title": (
                job.title
                if job
                else None
            ),
            "location": (
                job.location
                if job
                else None
            ),
            "job_url": (
                job.job_url
                if job
                else None
            ),
        },
    }