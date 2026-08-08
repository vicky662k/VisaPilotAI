from app.services.visa_detector import (
    detect_visa_sponsorship,
    detect_relocation_support,
)


test_cases = [
    {
        "name": "Sponsorship available",
        "text": "Visa sponsorship and relocation assistance are available.",
    },
    {
        "name": "No sponsorship",
        "text": "Candidates must already have authorization to work in the United States.",
    },
    {
        "name": "Work visa support",
        "text": "The company provides work visa support for qualified candidates.",
    },
    {
        "name": "Relocation only",
        "text": "Relocation assistance is available for this position.",
    },
]


for test in test_cases:
    visa = detect_visa_sponsorship(test["text"])
    relocation = detect_relocation_support(test["text"])

    print()
    print("Test:", test["name"])
    print("Visa sponsorship:", visa)
    print("Relocation support:", relocation)