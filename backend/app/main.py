from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.resume import router as resume_router
from app.api.v1.job import router as jobs_router
from app.api.v1.match import router as match_router
from app.api.v1.application_profile import (
    router as application_profile_router,
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Visa Sponsorship Job Finder",
)


@app.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running",
    }


app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX,
)


app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)


app.include_router(
    resume_router,
    prefix=settings.API_V1_PREFIX,
)


app.include_router(
    jobs_router,
    prefix=settings.API_V1_PREFIX,
)


app.include_router(
    match_router,
    prefix=settings.API_V1_PREFIX,
)


app.include_router(
    application_profile_router,
    prefix=settings.API_V1_PREFIX,
)

from app.api.v1.application import (
    router as application_router,
)

app.include_router(
    application_router,
    prefix=settings.API_V1_PREFIX,
)