import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.models.resume import Resume

from app.services.resume_service import create_resume
from app.services.ai_service import parse_resume_with_ai

from app.parser.resume_parser import extract_resume_text

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    allowed_extensions = [".pdf", ".docx"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

    unique_filename = f"{uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume = create_resume(
        db=db,
        filename=file.filename,
        filepath=file_path,
        user_id=current_user.id,
    )

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": resume.filename,
    }


@router.post("/parse/{resume_id}")
def parse_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    text = extract_resume_text(
        resume.file_path
    )

    parsed_resume = parse_resume_with_ai(text)

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "parsed_resume": parsed_resume,
    }