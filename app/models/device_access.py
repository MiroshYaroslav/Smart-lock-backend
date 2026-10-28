import uuid
from datetime import datetime, time
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Time, Boolean, ARRAY, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .devices import DeviceDB
    from .users import UserDB


class DeviceAccessDB(BaseDB):
    __tablename__ = "device_access"
    __table_args__ = (
        UniqueConstraint("user_id", "device_id", name="uix_user_device_access"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("devices.id", ondelete="CASCADE"))

    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    time_start: Mapped[Optional[time]] = mapped_column(Time)
    time_end: Mapped[Optional[time]] = mapped_column(Time)
    allowed_days: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer))

    can_open_remotely: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    user: Mapped["UserDB"] = relationship(lazy="raise")
    device: Mapped["DeviceDB"] = relationship(back_populates="access_rules", lazy="raise")
