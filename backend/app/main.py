from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Ensure all models are registered with Base

from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.devices import router as devices_router
from app.api.cameras import router as cameras_router
from app.api.security import router as security_router
from app.api.visitors import router as visitors_router
from app.api.automations import router as automations_router
from app.api.notifications import router as notifications_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure all tables exist on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SafeHome AI Smart Home Security & Automation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
origins = settings.CORS_ORIGINS
if isinstance(origins, str):
    import json
    origins = json.loads(origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Safe error reporting that avoids exposing internal stack traces
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again."}
    )


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Include API v1 Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(devices_router, prefix=settings.API_V1_STR)
app.include_router(cameras_router, prefix=settings.API_V1_STR)
app.include_router(security_router, prefix=settings.API_V1_STR)
app.include_router(visitors_router, prefix=settings.API_V1_STR)
app.include_router(automations_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
