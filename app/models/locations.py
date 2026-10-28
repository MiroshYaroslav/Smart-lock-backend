import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .users import UserDB
    from .location_member import LocationMemberDB
    from .devices import DeviceDB


class LocationDB(BaseDB):
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    owner: Mapped["UserDB"] = relationship(back_populates="owned_locations", lazy="raise")
    members: Mapped[List["LocationMemberDB"]] = relationship(back_populates="location", cascade="all, delete-orphan",
                                                           lazy="raise")
    devices: Mapped[List["DeviceDB"]] = relationship(back_populates="location", cascade="all, delete-orphan",
                                                   lazy="raise")