from sqlalchemy.orm import Session

from app.models.resume import Resume


def create_resume(
    db: Session,
    filename: str,
    filepath: str,
    user_id: int,
):

    resume = Resume(
        filename=filename,
        file_path=filepath,
        user_id=user_id,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume