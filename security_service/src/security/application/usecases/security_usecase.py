from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.common.logger import logger
from src.security.domain.services.repositories.security_repository import SecuritySqlRepository
from src.security.presentation.dto.security_dto import SecurityDataCreateDto, SecurityDataUpdateDto, \
    SecurityDataPartialUpdateDto


class SecurityUseCase:
    def __init__(self, security_repository: SecuritySqlRepository = Depends()):
        self.security_service = security_repository

    async def get_security_data(self, id: int):
        data = await self.security_service.get_by_id(id)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Security data not found"
            )

        return data

    async def create_security_data(self, security_data: SecurityDataCreateDto, user_id: int):
        try:
            return await self.security_service.create(security_data, user_id)

        except IntegrityError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Security data already exists"
            )

        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    async def delete_security_data(self, id: int):
        deleted_data = await self.security_service.delete(id)
        if not deleted_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Security data not found"
            )

        return deleted_data

    async def list_security_data(self, offset: int = 0, limit: int = 10):
        return await self.security_service.list(offset, limit)

    async def update_security_data(self, id: int, security_data: SecurityDataUpdateDto | SecurityDataPartialUpdateDto):
        updated_data = await self.security_service.update(id, security_data)
        if not updated_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Security data not found"
            )

        return updated_data
