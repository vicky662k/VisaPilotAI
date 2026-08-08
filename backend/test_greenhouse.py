from app.services.greenhouse_service import fetch_greenhouse_jobs


jobs = fetch_greenhouse_jobs("greenhouse")

print(f"Jobs found: {len(jobs)}")

for job in jobs[:5]:
    print()
    print("Title:", job.get("title"))
    print(
        "Location:",
        job.get("location", {}).get("name")
    )
    print("URL:", job.get("absolute_url"))