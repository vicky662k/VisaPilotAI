import re

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.match import JobMatch
from app.models.resume import Resume


# Skills and keywords relevant to your
# Technology Risk / IT Audit profile.

SKILL_ALIASES = {
    "itgc": [
        "itgc",
        "it general controls",
        "it general control",
    ],
    "it audit": [
        "it audit",
        "information technology audit",
        "technology audit",
    ],
    "technology risk": [
        "technology risk",
        "it risk",
        "technology risk management",
    ],
    "icfr": [
        "icfr",
        "internal control over financial reporting",
    ],
    "sap": [
        "sap",
        "sap ecc",
        "sap s/4hana",
        "sap s4hana",
        "s/4 hana",
    ],
    "access management": [
        "access management",
        "user access management",
        "identity and access management",
        "iam",
        "privileged access",
    ],
    "change management": [
        "change management",
        "change control",
        "change controls",
    ],
    "incident management": [
        "incident management",
        "incident response",
    ],
    "backup and recovery": [
        "backup and recovery",
        "backup & recovery",
        "disaster recovery",
    ],
    "it operations": [
        "it operations",
        "information technology operations",
    ],
    "cybersecurity": [
        "cybersecurity",
        "cyber security",
        "information security",
    ],
    "iso 27001": [
        "iso 27001",
        "iso/iec 27001",
    ],
    "sama": [
        "sama",
        "sama csf",
    ],
    "nca": [
        "nca",
        "nca ecc",
        "nca ecc-2018",
        "nca dcc",
    ],
    "pdpl": [
        "pdpl",
        "personal data protection law",
        "data privacy",
        "privacy compliance",
    ],
    "regulatory compliance": [
        "regulatory compliance",
        "regulatory controls",
        "regulatory requirements",
    ],
    "internal audit": [
        "internal audit",
        "internal auditing",
    ],
    "control testing": [
        "control testing",
        "controls testing",
        "control assessment",
        "control assessments",
    ],
    "risk management": [
        "risk management",
        "risk assessment",
        "risk assessments",
    ],
    "audit reporting": [
        "audit reporting",
        "audit reports",
        "audit findings",
    ],
    "stakeholder management": [
        "stakeholder management",
        "stakeholder communication",
    ],
    "project management": [
        "project management",
        "project coordination",
    ],
}


def normalize_text(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        (text or "").lower(),
    ).strip()


def extract_skills(text: str) -> set[str]:

    text = normalize_text(text)

    found_skills = set()

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if alias in text:
                found_skills.add(skill)
                break

    return found_skills


def calculate_skill_match(
    resume_text: str,
    job_description: str,
) -> float:

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    if not job_skills:
        return 0.0

    matched_skills = (
        resume_skills.intersection(job_skills)
    )

    score = (
        len(matched_skills)
        / len(job_skills)
    ) * 100

    return round(score, 2)


def get_skill_match_details(
    resume_text: str,
    job_description: str,
):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = sorted(
        resume_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    if not job_skills:
        skill_score = 0.0
    else:
        skill_score = round(
            (
                len(matched_skills)
                / len(job_skills)
            ) * 100,
            2,
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_score": skill_score,
    }


def extract_experience_requirement(
    job_description: str,
) -> int | None:

    text = normalize_text(job_description)

    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of)?\s*experience",
        r"minimum\s*(?:of)?\s*(\d+)\s*years?",
        r"at least\s*(\d+)\s*years?",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
        )

        if match:
            return int(match.group(1))

    return None


def extract_resume_experience(
    resume_text: str,
) -> int | None:

    text = normalize_text(resume_text)

    patterns = [
        r"over\s*(\d+)\s*years?",
        r"(\d+)\+?\s*years?\s*of\s*experience",
        r"(\d+)\+?\s*years?\s*experience",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
        )

        if match:
            return int(match.group(1))

    return None


def calculate_location_match(
    resume_text: str,
    job_location: str | None,
) -> float:

    if not job_location:
        return 0.0

    resume_text = normalize_text(resume_text)
    job_location = normalize_text(job_location)

    # Exact city matching
    city_aliases = {
        "abu dhabi": [
            "abu dhabi",
            "abudhabi",
        ],
        "dubai": [
            "dubai",
        ],
        "doha": [
            "doha",
        ],
        "riyadh": [
            "riyadh",
        ],
        "jeddah": [
            "jeddah",
        ],
        "manama": [
            "manama",
        ],
        "kuwait city": [
            "kuwait city",
        ],
        "muscat": [
            "muscat",
        ],
    }

    for city, aliases in city_aliases.items():

        if city in job_location:

            for alias in aliases:

                if alias in resume_text:
                    return 100.0

    # Country-level matching
    country_aliases = {
        "uae": [
            "uae",
            "united arab emirates",
        ],
        "united arab emirates": [
            "uae",
            "united arab emirates",
        ],
        "saudi arabia": [
            "saudi arabia",
            "ksa",
        ],
        "qatar": [
            "qatar",
        ],
        "bahrain": [
            "bahrain",
        ],
        "kuwait": [
            "kuwait",
        ],
        "oman": [
            "oman",
        ],
    }

    for country, aliases in country_aliases.items():

        if country in job_location:

            for alias in aliases:

                if alias in resume_text:
                    return 75.0

    # GCC regional relevance
    gcc_keywords = [
        "gcc",
        "gulf cooperation council",
        "middle east",
    ]

    if any(
        keyword in resume_text
        for keyword in gcc_keywords
    ):
        if any(
            country in job_location
            for country in [
                "uae",
                "united arab emirates",
                "saudi",
                "ksa",
                "qatar",
                "bahrain",
                "kuwait",
                "oman",
            ]
        ):
            return 50.0

    return 0.0


def calculate_visa_match(
    job: Job,
) -> bool:

    return bool(job.visa_sponsorship)


def calculate_overall_score(
    skill_score: float,
    visa_match: bool,
    location_score: float,
) -> float:

    visa_score = 100.0 if visa_match else 0.0

    overall_score = (
        skill_score * 0.60
        + visa_score * 0.20
        + location_score * 0.20
    )

    return round(overall_score, 2)


def create_job_match(
    db: Session,
    user_id: int,
    resume: Resume,
    job: Job,
):

    resume_text = resume.extracted_text or ""
    job_description = job.description or ""

    skill_details = get_skill_match_details(
        resume_text,
        job_description,
    )

    skill_score = skill_details["skill_score"]

    location_score = calculate_location_match(
        resume_text,
        job.location,
    )

    visa_match = calculate_visa_match(job)

    overall_score = calculate_overall_score(
        skill_score,
        visa_match,
        location_score,
    )

    existing_match = (
        db.query(JobMatch)
        .filter(
            JobMatch.user_id == user_id,
            JobMatch.job_id == job.id,
            JobMatch.resume_id == resume.id,
        )
        .first()
    )

    if existing_match:

        existing_match.match_score = overall_score
        existing_match.skill_match_score = skill_score
        existing_match.location_match = location_score
        existing_match.visa_match = visa_match

        db.commit()
        db.refresh(existing_match)

        return existing_match

    job_match = JobMatch(
        user_id=user_id,
        job_id=job.id,
        resume_id=resume.id,
        match_score=overall_score,
        skill_match_score=skill_score,
        location_match=location_score,
        visa_match=visa_match,
    )

    db.add(job_match)
    db.commit()
    db.refresh(job_match)

    return job_match
def match_resume_to_all_jobs(
    db: Session,
    user_id: int,
    resume: Resume,
):
    jobs = (
        db.query(Job)
        .order_by(Job.id)
        .all()
    )

    matches = []

    for job in jobs:

        match = create_job_match(
            db=db,
            user_id=user_id,
            resume=resume,
            job=job,
        )

        matches.append(match)

    # Visa-sponsored jobs first,
    # then highest overall match score.
    matches.sort(
        key=lambda match: (
            bool(match.visa_match),
            match.match_score or 0,
        ),
        reverse=True,
    )

    return matches
def match_active_jobs_for_resume(
    db: Session,
    user_id: int,
    resume: Resume,
):
    jobs = (
        db.query(Job)
        .filter(
            Job.is_active == True,
        )
        .order_by(Job.id)
        .all()
    )

    matches = []

    for job in jobs:

        match = create_job_match(
            db=db,
            user_id=user_id,
            resume=resume,
            job=job,
        )

        matches.append(match)

    # Visa-sponsored jobs first,
    # then highest overall match score.
    matches.sort(
        key=lambda match: (
            bool(match.visa_match),
            match.match_score or 0,
        ),
        reverse=True,
    )

    return matches