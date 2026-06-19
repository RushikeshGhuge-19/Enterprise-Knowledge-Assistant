from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from test.config import settings

# Database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
