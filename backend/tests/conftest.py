"""Pytest fixtures for testing."""
import sys
import os
from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, get_db
from app import app


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database dependency."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_school_year():
    """Return sample school year data."""
    return {
        "name": "2024/2025",
        "start_date": "2024-09-01",
        "end_date": "2025-07-31",
        "is_active": True
    }


@pytest.fixture
def sample_class():
    """Return sample class data."""
    return {"name": "Class 1A"}


@pytest.fixture
def sample_pupil():
    """Return sample pupil data."""
    return {"first_name": "Max", "last_name": "Mustermann"}


@pytest.fixture
def sample_category():
    """Return sample category data."""
    return {
        "name_de": "Test Kategorie",
        "name_en": "Test Category",
        "is_predefined": False
    }


@pytest.fixture
def sample_entry():
    """Return sample entry data."""
    return {
        "date": str(date.today()),
        "text": "Test entry text",
        "grade": "A",
        "subject": "Math"
    }
