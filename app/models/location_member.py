import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from .enums import MemberRole
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .locations import LocationDB
    from .users import UserDB


class LocationMemberDB(BaseDB):
    __tablename__ = "location_members"
    __table_args__ = (
        UniqueConstraint("location_id", "user_id", name="uix_location_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole, name="member_role_enum"), default=MemberRole.guest)

    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    location: Mapped["LocationDB"] = relationship(back_populates="members", lazy="raise")
    user: Mapped["UserDB"] = relationship(back_populates="memberships", lazy="raise")