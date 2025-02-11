from datetime import datetime
from typing import Dict, Generator

from fastapi.testclient import TestClient

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.security import create_token
from app.db.base import Base
from app.main import app
from app.models.user import User

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """Create a fresh database for each test."""
    Base.metadata.drop_all(bind=engine)  # Clean up before test
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up after test


@pytest.fixture
def client(db) -> Generator:
    """Create a new FastAPI TestClient that uses the `db` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def normal_user(db: TestingSessionLocal) -> User:
    """Create a normal user for testing."""
    try:
        db.rollback()  # Reset any failed transaction
        user = User(
            email="user@example.com",
            username="testuser",
            is_active=True,
            is_superuser=False,
            date_joined=datetime.now(),
        )
        user.set_password("testpass123")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


@pytest.fixture
def superuser(db: TestingSessionLocal) -> User:
    """Create a superuser for testing."""
    try:
        db.rollback()  # Reset any failed transaction
        user = User(
            email="admin@example.com",
            username="admin",
            is_active=True,
            is_superuser=True,
            date_joined=datetime.now(),
        )
        user.set_password("adminpass123")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


@pytest.fixture
def inactive_user(db: TestingSessionLocal) -> User:
    """Create an inactive user for testing."""
    try:
        db.rollback()  # Reset any failed transaction
        user = User(
            email="inactive@example.com",
            username="inactive",
            is_active=False,
            date_joined=datetime.now(),
        )
        user.set_password("inactive123")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


@pytest.fixture
def normal_user_token_headers(normal_user: User) -> Dict[str, str]:
    """Return authorization headers for normal user."""
    return {"Authorization": f"Bearer {create_token(str(normal_user.id))}"}


@pytest.fixture
def superuser_token_headers(superuser: User) -> Dict[str, str]:
    """Return authorization headers for superuser."""
    return {"Authorization": f"Bearer {create_token(str(superuser.id))}"}
