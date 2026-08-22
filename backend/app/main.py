from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.resume import router as resume_router
from app.api.v1.job import router as jobs_router
from app.api.v1.match import router as match_router
from app.api.v1.application_profile import (
    router as application_profile_router,
)
from app.api.v1.application import (
    router as application_router,
)
from app.api.v1.application_data import (
    router as application_data_router,
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Visa Sponsorship Job Finder",
)


# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running",
    }


# ===============================
# API ROUTES
# ===============================

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

app.include_router(
    application_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    application_data_router,
    prefix=settings.API_V1_PREFIX,
)