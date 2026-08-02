from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Visa Sponsorship Job Finder"
)


@app.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }

app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX
)