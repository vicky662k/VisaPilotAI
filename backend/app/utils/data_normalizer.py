import re


def normalize_email(
    value: str | None,
) -> str | None:
    if not value:
        return value

    value = value.strip()

    # Convert Markdown email:
    # [name@example.com](mailto:name@example.com)
    # into:
    # name@example.com
    match = re.fullmatch(
        r"\[([^\]]+)\]\(mailto:[^)]+\)",
        value,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(1).strip()

    return value