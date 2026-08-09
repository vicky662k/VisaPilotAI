def normalize_email(
    value: str | None,
) -> str | None:
    if not value:
        return value

    value = value.strip()

    if value.startswith("["):
        end = value.find("]")

        if end > 1:
            email = value[1:end].strip()

            if "@" in email:
                return email

    return value