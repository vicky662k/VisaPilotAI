import re


SPONSORSHIP_PATTERNS = [
    r"visa sponsorship",
    r"sponsorship available",
    r"will sponsor",
    r"visa support",
    r"work visa support",
    r"employment visa",
    r"work permit sponsorship",
    r"sponsor.*visa",
    r"visa.*sponsor",
]


RELOCATION_PATTERNS = [
    r"relocation support",
    r"relocation assistance",
    r"relocation package",
    r"relocation provided",
    r"relocation available",
    r"support relocation",
]


def detect_visa_sponsorship(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    for pattern in SPONSORSHIP_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


def detect_relocation_support(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    for pattern in RELOCATION_PATTERNS:
        if re.search(pattern, text):
            return True

    return False