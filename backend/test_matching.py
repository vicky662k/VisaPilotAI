from app.database.database import SessionLocal
from app.models.resume import Resume
from app.services.matching_service import extract_skills


db = SessionLocal()

resume = (
    db.query(Resume)
    .filter(Resume.id == 1)
    .first()
)

if resume is None:
    print("Resume not found")
else:
    skills = extract_skills(
        resume.extracted_text or ""
    )

    print("\nDetected skills:")
    print("----------------")

    for skill in sorted(skills):
        print(f"✓ {skill}")

    print("\nTotal skills:", len(skills))

db.close()