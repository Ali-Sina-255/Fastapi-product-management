from apps.core.config import settings
from apps.core.logging import get_logger
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import text
from typing import Generator

logger = get_logger()

# PostgreSQL engine configuration
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,  # Number of connections to keep open
    max_overflow=10,  # Extra connections beyond pool_size
    pool_recycle=3600,  # Recycle connections after 1 hour
)


def init_db() -> None:
    """Initialize database - create all tables"""
    try:
        logger.info("Connecting to Supabase PostgreSQL...")
        logger.info(
            f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Supabase'}"
        )

        # Test connection - FIX: Wrap SQL with text()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()
            logger.info(
                f"✅ Connected to PostgreSQL: {version[0].split(',')[0] if version else 'Unknown'}"
            )

        # Create tables
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Database tables created successfully")

    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
