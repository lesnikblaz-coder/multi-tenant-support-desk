from uuid import UUID
from sqlalchemy import String, BOOLEAN, Text, text
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        server_default=text("true")
    )

    memberships: Mapped[list["OrganizationMembership"]] = relationship(
        back_populates="user"
    )