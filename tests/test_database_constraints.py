import pytest

from sqlalchemy.exc import IntegrityError

from src.db.models.user import User


def _create_user() -> User:
    return User(
        email="test@email.com",
        password_hash="testpasswordhash123",
    )

async def test_user_creation(
        test_session_factory
) -> None:
    """Create a user, verify PostgreSQL generates its UUID and sets is_active to True."""

    user = _create_user()

    async with test_session_factory.begin() as session:
        session.add(user)

    # expire_on_commit=False allows this
    assert user.id is not None
    assert user.is_active is True


async def test_duplicate_email_rejected(
        test_session_factory
) -> None:
    """Verify that users cannot have the same email."""

    user = _create_user()

    async with test_session_factory.begin() as session:
        session.add(user)

    user2 = _create_user()

    with pytest.raises(IntegrityError):
        async with test_session_factory.begin() as session:
            session.add(user2)