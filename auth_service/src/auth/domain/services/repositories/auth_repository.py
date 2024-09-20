from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.models.entities.user_sql_model import UserEntity
from src.auth.inferastractor.database import get_db_session
from src.auth.presentation.dto.auth_dto import UserCreateDTO


class UserSqlRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        user = (await self.db.scalar(
            select(UserEntity).where(UserEntity.email == email)
        ))
        if not user:
            return None

        return user

    async def create_user(self, user: UserCreateDTO):
        try:
            user = UserEntity(**user.dict())
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user

        except Exception as e:
            await self.db.rollback()
            raise e
