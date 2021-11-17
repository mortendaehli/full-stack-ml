from typing import Generator

from app.config import config
from app.entities import Account, Base, Role, User, UserRole  # noqa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
