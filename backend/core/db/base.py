from sqlalchemy import create_engine
from typing import Generator
from settings.config import settings, SQLITE_DB_URL
from sqlalchemy.orm import sessionmaker

# Read more here:
# https://fastapi.tiangolo.com/tutorial/sql-databases/
engine = create_engine(settings.database_url or SQLITE_DB_URL , pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bin=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
