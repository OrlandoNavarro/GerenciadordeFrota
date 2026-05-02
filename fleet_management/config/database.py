from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings
from urllib.parse import urlparse
import os


def _normalize_sqlite_url(url: str) -> str:
    # Accept formats like sqlite:///./fleet_management.db
    return url


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    _normalize_sqlite_url(DATABASE_URL),
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
