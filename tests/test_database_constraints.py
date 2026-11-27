from src.db.models.user import User


async def test_user_creation(
        test_session_factory
):
    """Create a user, verify PostgreSQL generates its UUID and sets is_active to True."""

    user = User(
        email="test@email.com",
        password_hash="testpasswordhash123",
    )

    async with test_session_factory.begin() as session:
        session.add(user)

    assert user.id is not None
    assert user.is_active is True