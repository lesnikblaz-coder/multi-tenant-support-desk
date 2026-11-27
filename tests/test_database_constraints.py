import pytest

from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from src.db.models.user import User
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

    with pytest.raises(IntegrityError) as exc_info:
        async with test_session_factory.begin() as session:
            session.add(user2)

    assert exc_info.value.orig.sqlstate == "23505"


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
        session.add_all([user, org1, org2])

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
        session.add_all([membership1, membership2])

    assert membership1.user_id == membership2.user_id

    async with test_session_factory.begin() as session:
        stmt = (
            select(User)
            .where(User.email == user.email)
            .options(
                selectinload(User.memberships)
            )
        )

        result = await session.execute(stmt)

        db_user = result.scalar_one_or_none()

    assert db_user
    assert len(db_user.memberships) == 2

    org_to_role = {
        m.organization_id: m.role
        for m in db_user.memberships
    }

    assert org_to_role == {
        membership1.organization_id: membership1.role,
        membership2.organization_id: membership2.role
    }


async def test_duplicate_membership_rejected(
        test_session_factory,
        user_factory,
        organization_factory
) -> None:
    """Composite primary key successfully prevents duplicate memberships."""

    user = user_factory("user")
    org = organization_factory("Test Organization")

    async with test_session_factory.begin() as session:
        session.add_all([user, org])

    membership1 = OrganizationMembership(
        user_id=user.id,
        organization_id=org.id,
        role=UserRole.ADMIN
    )

    async with test_session_factory.begin() as session:
        session.add(membership1)

    membership2 = OrganizationMembership(
        user_id=user.id,
        organization_id=org.id,
        role=UserRole.MEMBER
    )

    with pytest.raises(IntegrityError) as exc_info:
        async with test_session_factory.begin() as session:
            session.add(membership2)

    assert exc_info.value.orig.sqlstate == "23505"


async def test_membership_with_nonexistent_user_rejected(
        test_session_factory,
        organization_factory
) -> None:
    """A membership with a valid organization (ID) but a nonexistent user (ID) gets rejected."""

    org = organization_factory("Test Organization")

    async with test_session_factory.begin() as session:
        session.add(org)

    membership1 = OrganizationMembership(
        user_id=uuid4(),
        organization_id=org.id,
        role=UserRole.ADMIN
    )

    with pytest.raises(IntegrityError) as exc_info:
        async with test_session_factory.begin() as session:
            session.add(membership1)

    assert exc_info.value.orig.sqlstate == "23503"


async def test_membership_with_nonexistent_organization_rejected(
        test_session_factory,
        user_factory
) -> None:
    """A membership with a valid user (ID) but a nonexistent organization (ID) gets rejected."""

    user = user_factory("user")

    async with test_session_factory.begin() as session:
        session.add(user)

    membership1 = OrganizationMembership(
        user_id=user.id,
        organization_id=uuid4(),
        role=UserRole.ADMIN
    )

    with pytest.raises(IntegrityError) as exc_info:
        async with test_session_factory.begin() as session:
            session.add(membership1)

    assert exc_info.value.orig.sqlstate == "23503"