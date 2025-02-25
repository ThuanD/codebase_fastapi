from datetime import datetime
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.security import create_token
from app.db.base import Base
from app.main import app
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(async_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a new FastAPI TestClient that uses the `db` fixture."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield async_db
        finally:
            await async_db.close()

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def normal_user(async_db: AsyncSession) -> User:
    """Create a normal user for testing."""
    user = User(
        email="user@example.com",
        username="testuser",
        is_active=True,
        is_superuser=False,
        date_joined=datetime.now(),
    )
    user.set_password("testpass123")
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def superuser(async_db: AsyncSession) -> User:
    """Create a superuser for testing."""
    user = User(
        email="admin@example.com",
        username="admin",
        is_active=True,
        is_superuser=True,
        date_joined=datetime.now(),
    )
    user.set_password("adminpass123")
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def inactive_user(async_db: AsyncSession) -> User:
    """Create an inactive user for testing."""
    user = User(
        email="inactive@example.com",
        username="inactive",
        is_active=False,
        date_joined=datetime.now(),
    )
    user.set_password("inactive123")
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def normal_user_token_headers(normal_user: User) -> dict[str, str]:
    """Return authorization headers for normal user."""
    return {"Authorization": f"Bearer {create_token(str(normal_user.id))}"}


@pytest_asyncio.fixture
async def superuser_token_headers(superuser: User) -> dict[str, str]:
    """Return authorization headers for superuser."""
    return {"Authorization": f"Bearer {create_token(str(superuser.id))}"}
