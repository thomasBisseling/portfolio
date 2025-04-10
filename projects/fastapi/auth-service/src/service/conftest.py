import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, SQLModel

from service import app
from service.core.cli import call_command
from service.core.database import db_connection


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_engine():
    engine = create_async_engine(
        db_connection.get_db_url(), poolclass=NullPool, echo=False
    )
    yield engine


@pytest.fixture(name="db_session")
async def async_session(async_engine):
    session_maker = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with session_maker() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture(autouse=True)
async def mock_db_dependency(db_session):
    """Override the database dependency for testing."""

    async def override_get_session():
        yield db_session

    app.dependency_overrides[db_connection.get_async_session] = override_get_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    db_url = db_connection.get_db_url()
    if database_exists(db_url):
        drop_database(db_url)
    create_database(db_url)
    call_command("migrate", silent=True)
    yield  # Run the tests
    drop_database(db_url)


@pytest.fixture(name="client", scope="function")
def client_fixture(setup_database):
    with TestClient(app) as test_client:
        yield test_client
