from uuid import UUID
from sqlalchemy import String, text
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(
        SQL_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    memberships: Mapped[list["OrganizationMembership"]] = relationship(
        back_populates="organization"
    )