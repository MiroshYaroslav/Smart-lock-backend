from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.users import UserRepository
from app.schemas.token import Token
from app.schemas.users import UserCreate
from app.services.base import BaseService


class AuthService(BaseService):
    def __init__(self, session: AsyncSession, user_repo: UserRepository):
        super().__init__(session)
        self.user_repo = user_repo

    async def register_new_user(self, user_in: UserCreate):
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        password_hash = get_password_hash(user_in.password)

        user_data = user_in.model_dump(exclude={"password"})
        user_data["password_hash"] = password_hash
        user_data["is_active"] = True

        new_user = await self.user_repo.create(user_data)

        await self._session.commit()

        return new_user

    async def authenticate_user(self, email: str, password: str) -> Token:
        user = await self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")