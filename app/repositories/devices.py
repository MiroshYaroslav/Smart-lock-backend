from sqlalchemy import select
from app.models.devices import DeviceDB
from app.repositories.base import BaseRepository

class DeviceRepository(BaseRepository[DeviceDB]):
    _model = DeviceDB

    async def get_by_mac_address(self, mac_address: str) -> DeviceDB | None:
        stmt = select(self._model).where(self._model.mac_address == mac_address)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()