import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from .enums import DeviceStatus
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .locations import LocationDB
    from .device_access import DeviceAccessDB


class DeviceDB(BaseDB):
    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))
    mac_address: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[DeviceStatus] = mapped_column(Enum(DeviceStatus, name="device_status_enum"), default=DeviceStatus.offline)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    location: Mapped["LocationDB"] = relationship(back_populates="devices", lazy="raise")
    access_rules: Mapped[List["DeviceAccessDB"]] = relationship(back_populates="device", cascade="all, delete-orphan",
                                                              lazy="raise")