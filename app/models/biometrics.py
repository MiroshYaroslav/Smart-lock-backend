import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, ARRAY, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseDB
from ..core.datetime_utils import get_time

if TYPE_CHECKING:
    from .users import UserDB


class BiometricsDB(BaseDB):
    __tablename__ = "biometrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    face_embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float))
    voice_embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float))
    s3_photo_key: Mapped[Optional[str]] = mapped_column(String)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_time, onupdate=get_time)

    user: Mapped["UserDB"] = relationship(back_populates="biometrics", lazy="raise")