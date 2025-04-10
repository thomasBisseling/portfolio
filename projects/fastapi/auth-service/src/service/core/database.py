import sys

from fastapi import (
    HTTPException,
)
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, SQLModel, create_engine

from service.core.settings import settings


class DatabaseEngineError(Exception):
    """Database engine error."""

    pass


class DatabaseConnection:
    """Database connection class."""

    def __init__(self):
        self._host_url = None
        self._engine_async: AsyncEngine | None = None
        self._engine_sync = None
        self._async_session_factory = None
        self._sync_session_factory = None

    @staticmethod
    def _get_engine_type() -> str:
        """Get the database engine.

        Only supports PostgreSQL and SQLite.
        """
        if settings.db_engine == "postgresql":
            return "postgresql+psycopg"
        elif settings.db_engine == "sqlite":
            return "sqlite"
        raise DatabaseEngineError(
            f"Database engine '{settings.db_engine}' not supported."
        )

    @staticmethod
    def _get_host_url(engine_type: str) -> str:
        """Get the host URL for the database engine."""
        if engine_type == "sqlite":
            return f"{engine_type}:///"

        return (
            f"{engine_type}://"
            f"{settings.db_user}:{settings.db_password}@"
            f"{settings.db_host}:{settings.db_port}"
        )

    def get_db_url(self) -> str:
        """Get the database URL."""
        db_url = settings.db_url
        if db_url is None:
            host_url = self._get_host_url(self._get_engine_type())
            db_url = f"{host_url}/{settings.db_name}"
        return db_url

    def _get_or_create_sync_engine(self):
        """Get or create a synchronous engine."""
        if self._engine_sync is None:
            db_url = self.get_db_url()
            if not database_exists(db_url):
                create_database(db_url)
            self._engine_sync = create_engine(
                db_url,
                echo=settings.db_sql_log,
                future=True,
                pool_pre_ping=True,
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                pool_timeout=settings.db_pool_timeout,
            )
        return self._engine_sync

    def _get_or_create_async_engine(self) -> AsyncEngine:
        """Get or create an async engine."""
        if self._engine_async is None:
            db_url = self.get_db_url()
            if not database_exists(db_url):
                create_database(db_url)
            self._engine_async = create_async_engine(
                db_url,
                echo=settings.db_sql_log,
                future=True,
                pool_pre_ping=True,
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                pool_timeout=settings.db_pool_timeout,
            )
        return self._engine_async

    def get_or_create_engine(self, async_engine=False):
        """Get or create the database engine.

        Args:
            async_engine (bool): Whether to create an async engine.
        """

        if async_engine:
            return self._get_or_create_async_engine()
        return self._get_or_create_sync_engine()

    def dispose_sync(self):
        """Dispose the synchronous database engine."""
        if self._engine_sync is not None:
            self._engine_sync.dispose()
        self._engine_sync = None

    async def dispose_async(self):
        """Dispose the asynchronous database engine."""
        if self._engine_async is not None:
            await self._engine_async.dispose()
        self._engine_async = None

    async def dispose(self):
        """Dispose the database engine.

        Disposes both the synchronous and asynchronous engines.
        """

        await self.dispose_async()
        self.dispose_sync()

    def _get_or_create_sync_session_factory(self):
        engine = self.get_or_create_engine(False)
        if not self._sync_session_factory:
            self._sync_session_factory = sessionmaker(
                bind=engine,
                class_=Session,
                expire_on_commit=True,
            )
        return self._sync_session_factory

    def _get_or_create_async_session_factory(self):
        engine = self.get_or_create_engine(True)
        if not self._async_session_factory:
            self._async_session_factory = sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=True,
            )
        return self._async_session_factory

    async def get_async_session(self):
        """Get an async session."""
        session_factory = self._get_or_create_async_session_factory()

        async with session_factory() as session:
            yield session
            try:
                await session.commit()  # Explicit commit
            except OperationalError:  # Handle disconnection issues
                raise HTTPException(status_code=503, detail="Database connection lost")
            except SQLAlchemyError:
                raise HTTPException(status_code=500, detail="Database error")

    def get_sync_session(self):
        """Get a sync session.

        THIS IS ONLY FOR TESTING PURPOSES. THIS IS USED FOR FACTORIES ONLY.
        """
        session_factory = self._get_or_create_sync_session_factory()
        session = session_factory()

        try:
            session.commit()  # Explicit commit
        except OperationalError:
            session.rollback()
            raise HTTPException(status_code=503, detail="Database connection lost")
        except SQLAlchemyError:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            session.close()
        return session


db_connection = DatabaseConnection()
