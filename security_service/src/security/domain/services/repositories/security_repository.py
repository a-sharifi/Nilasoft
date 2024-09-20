from typing import Tuple, Sequence, Dict, Any

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.logger import logger
from src.common.database import get_db_session
from src.security.domain.models.entities.security_sql_model import SecurityDataEntity
from src.security.presentation.dto.security_dto import (SecurityDataCreateDto,
                                                        SecurityDataUpdateDto,
                                                        SecurityDataPartialUpdateDto)


class SecuritySqlRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db

    async def get_by_id(self, id: int) -> SecurityDataEntity | None:
        security = await self.db.scalar(
            select(SecurityDataEntity).where(SecurityDataEntity.id == id)
        )
        if not security:
            return None

        return security

    async def create(self, security: SecurityDataCreateDto, user_id) -> SecurityDataEntity | None:
        try:
            security = SecurityDataEntity(**security.dict(), user_id=user_id)
            self.db.add(security)
            await self.db.commit()
            await self.db.refresh(security)
            return security

        except IntegrityError as e:
            logger.error("Integrity error: %s", e)
            await self.db.rollback()
            raise e

        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete(self, id: int) -> SecurityDataEntity | None:
        security = await self.get_by_id(id)
        if not security:
            return None

        await self.db.delete(security)
        await self.db.commit()
        return security

    async def list(self, offset: int = 0, limit: int = 10) -> Tuple[Sequence[SecurityDataEntity], Dict[str, Any]]:
        total = await self.db.scalar(select(func.count()).select_from(SecurityDataEntity))
        logger.info(f"Total securities: {total}")

        result = await self.db.execute(
            select(SecurityDataEntity).offset(offset).limit(limit)
        )
        securities = result.scalars().all()

        return securities, {"offset": offset, "limit": limit, "total": total}

    async def update(self, id: int,
                     security_dto: SecurityDataUpdateDto | SecurityDataPartialUpdateDto) -> SecurityDataEntity | None:
        security = await self.get_by_id(id)
        if not security:
            return None

        for field, value in security_dto.model_dump(exclude_none=True).items():
            setattr(security, field, value)

        await self.db.commit()
        await self.db.refresh(security)
        return security
