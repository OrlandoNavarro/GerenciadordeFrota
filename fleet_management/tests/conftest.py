import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.connection import Base
import os


@pytest.fixture(scope='function')
def db_session(tmp_path):
    db_file = tmp_path / 'test.db'
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
