from app.db.database import get_session_dep
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import UserRepository
from app.services.auth import AuthService


async def get_user_repo(session: AsyncSession = Depends(get_session_dep)) -> UserRepository:
    return UserRepository(session)


async def get_auth_service(
    session: AsyncSession = Depends(get_session_dep),
    user_repo: UserRepository = Depends(get_user_repo)
) -> AuthService:
    return AuthService(session=session, user_repo=user_repo)