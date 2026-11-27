import pytest

from sqlalchemy.exc import IntegrityError

from src.db.models.organization_membership import OrganizationMembership
from src.enums import UserRole


async def test_user_creation(
        test_session_factory,
        user_factory
) -> None:
    """Create a user, verify PostgreSQL generates its UUID and sets is_active to True."""

    user = user_factory("user1")

    async with test_session_factory.begin() as session:
        session.add(user)

    # expire_on_commit=False allows this
    assert user.id is not None
    assert user.is_active is True


async def test_duplicate_email_rejected(
        test_session_factory,
        user_factory
) -> None:
    """Verify that users cannot have the same email."""

    user = user_factory("user1")

    async with test_session_factory.begin() as session:
        session.add(user)

    user2 = user_factory("user1")

    with pytest.raises(IntegrityError):
        async with test_session_factory.begin() as session:
            session.add(user2)


async def test_user_can_belong_to_multiple_organizations(
        test_session_factory,
        user_factory,
        organization_factory
) -> None:
    """Same user with a membership in two organizations with different roles succeeds."""

    user = user_factory("user")
    org1 = organization_factory("Test Organization 1")
    org2 = organization_factory("Test Organization 2")


    async with test_session_factory.begin() as session:
        session.add(user)
        session.add(org1)
        session.add(org2)

    membership1 = OrganizationMembership(
        user_id=user.id,
        organization_id=org1.id,
        role=UserRole.ADMIN
    )

    membership2 = OrganizationMembership(
        user_id=user.id,
        organization_id=org2.id,
        role=UserRole.MEMBER
    )

    async with test_session_factory.begin() as session:
        session.add(membership1)
        session.add(membership2)

    assert membership1.user_id == membership2.user_id
    assert membership1.role == UserRole.ADMIN
    assert membership2.role == UserRole.MEMBER
    assert membership1.removed_at is None
    assert membership2.removed_at is None