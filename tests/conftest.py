import pytest
import pytest_asyncio

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.db.base import Base
from src.db.models.user import User
from src.db.models.organization import Organization

test_async_engine = create_async_engine(
    url=settings.test_async_db_url,
    poolclass=NullPool
)


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
    autouse=True
)
async def setup_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_session_factory():
    async with test_async_engine.connect() as connection:
        transaction = await connection.begin()

        session_factory = async_sessionmaker(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint"
        )

        try:
            yield session_factory

        finally:
            await transaction.rollback()


@pytest.fixture
def user_factory():
    def _create_user(email_prefix: str) -> User:
        return User(
            email=f"{email_prefix}@test.com",
            password_hash="testpasswordhash123"
        )

    return _create_user


@pytest.fixture
def organization_factory():
    def _create_org(name: str) -> Organization:
        return Organization(name=name)

    return _create_org