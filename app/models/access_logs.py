import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from .enums import AccessStatus
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .users import UserDB


class AccessLogDB(BaseDB):
    __tablename__ = "access_logs"
    __table_args__ = (
        Index("ix_access_logs_device_timestamp", "device_id", "timestamp"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("devices.id", ondelete="CASCADE"))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    status: Mapped[AccessStatus] = mapped_column(Enum(AccessStatus, name="access_status_enum"), nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String)
    s3_photo_key: Mapped[Optional[str]] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time)

    user: Mapped[Optional["UserDB"]] = relationship(back_populates="access_logs")
