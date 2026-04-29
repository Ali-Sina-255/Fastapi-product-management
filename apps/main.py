from fastapi import FastAPI
from apps.core.config import settings
from contextlib import asynccontextmanager
from apps.api.main import api_router
from apps.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    init_db()
    yield
    print("Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


app.include_router(api_router, prefix=settings.API_V1_STR)
