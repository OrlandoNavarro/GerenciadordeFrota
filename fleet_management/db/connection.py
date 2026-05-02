from sqlalchemy.orm import declarative_base
from config.database import engine, SessionLocal

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
