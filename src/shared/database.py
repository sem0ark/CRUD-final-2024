from typing import Generator

from sqlalchemy import Select, create_engine, func, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.shared.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# instance will be the session

Base = declarative_base()  # will be used to make models


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # a "proxy" of a SQLAlchemy Session
    try:
        yield db
    finally:
        db.close()
    # This way we make sure the database session is always closed after the request.


def paginate(session: Session, query: Select, limit: int, offset: int) -> dict:
    return {
        "count": session.scalar(select(func.count()).select_from(query.subquery())),
        "items": list(session.scalars(query.limit(limit).offset(offset))),
    }
