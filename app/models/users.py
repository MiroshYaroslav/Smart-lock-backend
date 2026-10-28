import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .biometrics import BiometricsDB
    from .locations import LocationDB
    from .location_member import LocationMemberDB
    from .access_logs import AccessLogDB


class UserDB(BaseDB):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    biometrics: Mapped["BiometricsDB"] = relationship(back_populates="user", uselist=False, lazy="raise")
    owned_locations: Mapped[List["LocationDB"]] = relationship(back_populates="owner", lazy="raise")
    memberships: Mapped[List["LocationMemberDB"]] = relationship(back_populates="user", lazy="raise")
    access_logs: Mapped[list["AccessLogDB"]] = relationship(back_populates="user", lazy="raise")