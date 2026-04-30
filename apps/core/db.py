from apps.core.logging import get_logger
from sqlmodel import create_engine, Session, SQLModel
import psycopg2

logger = get_logger()
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def init_db() -> None:
    try:
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
