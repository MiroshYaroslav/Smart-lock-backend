from sqlalchemy import select
from app.models.users import UserDB
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[UserDB]):
    _model = UserDB

    async def get_by_email(self, email: str) -> UserDB | None:
        stmt = select(self._model).where(self._model.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()