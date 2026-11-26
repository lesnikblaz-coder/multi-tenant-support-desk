from uuid import UUID
from sqlalchemy import Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.db.base import Base
from src.enums import UserRole


class OrganizationMembership(Base):
    __tablename__ = "organization_memberships"

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id"),
        primary_key=True
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.MEMBER
    )
    removed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="memberships"
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="memberships"
    )