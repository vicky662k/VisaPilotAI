import re


def clean_text(value: str | None) -> str:
    """
    Normalize whitespace in text fields.
    """
    if not value:
        return ""

    return re.sub(
        r"\s+",
        " ",
        value,
    ).strip()


def normalize_company(company: str | None) -> str:
    """
    Clean company name.
    """
    return clean_text(company)


def normalize_title(title: str | None) -> str:
    """
    Clean job title.
    """
    return clean_text(title)


def normalize_location(location: str | None) -> str | None:
    """
    Clean job location.
    """
    if not location:
        return None

    cleaned = clean_text(location)

    return cleaned or None


def normalize_description(
    description: str | None,
) -> str:
    """
    Clean job description while preserving
    the actual content.
    """
    return clean_text(description)


def normalize_job_data(
    *,
    company: str | None,
    title: str | None,
    location: str | None,
    description: str | None,
    job_url: str | None,
    source: str | None,
) -> dict:

    return {
        "company": normalize_company(company),
        "title": normalize_title(title),
        "location": normalize_location(location),
        "description": normalize_description(description),
        "job_url": clean_text(job_url),
        "source": clean_text(source),
    }