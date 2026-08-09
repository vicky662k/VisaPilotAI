from app.services.job_normalizer import (
    normalize_job_data,
)


result = normalize_job_data(
    company="  Greenhouse  ",
    title="  Technology Risk Consultant   ",
    location="  Abu Dhabi, UAE  ",
    description="This   is   a   sample job description.",
    job_url=" https://example.com/job/1 ",
    source=" greenhouse ",
)


print("\n===== M6.3 NORMALIZER TEST =====")

for key, value in result.items():
    print(f"{key}: {value}")