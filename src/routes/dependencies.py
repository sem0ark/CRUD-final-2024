from src.data.database import SessionLocal


def get_db():
    db = SessionLocal()  # a "proxy" of a SQLAlchemy Session
    try:
        yield db
    finally:
        db.close()
    # This way we make sure the database session is always closed after the request.
