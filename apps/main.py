from fastapi import FastAPI, Depends
from apps.core.config import settings
from contextlib import asynccontextmanager
from apps.api.main import api_router

# from apps.core.db import init_db
from apps.core.database import init_db, get_session
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting application...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Connecting to database...")
    init_db()  # This will create all tables
    print("✅ Application ready!")
    yield
    # Shutdown
    print("👋 Shutting down application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.get("/test-db")
def test_db(session: Session = Depends(get_session)):
    from sqlmodel import text

    result = session.exec(text("SELECT 1 as test")).first()
    return {"status": "connected", "test": result}


app.include_router(api_router, prefix=settings.API_V1_STR)
