import uuid # Додаємо імпорт
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.access_logs import AccessLogDB
from app.repositories.base import BaseRepository

class AccessLogRepository(BaseRepository[AccessLogDB]):
    _model = AccessLogDB

    async def get_device_logs(self, device_id: uuid.UUID, limit: int = 50) -> list[AccessLogDB]:
        stmt = (
            select(self._model)
            .where(self._model.device_id == device_id)
            .options(joinedload(self._model.user))
            .order_by(self._model.timestamp.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())