from fastapi import APIRouter, status, Depends, Security

from src.common.dto.pagination_dto import LimitOffsetPaginationParamDTO
from src.common.guards.auth_gurad import AuthGuard
from src.common.response import CRUDSummaryDescription, ResponseMessages, ApiResponse, MetaData
from src.security.application.usecases.security_usecase import SecurityUseCase
from src.security.presentation.dto.security_dto import (SecurityDataCreateDto,
                                                        SecurityDataUpdateDto,
                                                        SecurityDataPartialUpdateDto)
from src.security.presentation.serializers.security_serializer import SecurityDataSerializer

object_name = "Security Data"
crud_handler = CRUDSummaryDescription(object_name=object_name)
response_messages = ResponseMessages(object_name=object_name)

auth = AuthGuard()

router = APIRouter(prefix="/security", tags=[object_name])


@router.get(
    "/",
    response_model=ApiResponse[list[SecurityDataSerializer]],
    summary=crud_handler.fetch_summary,
    description=crud_handler.fetch_description,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def list_securities_data(
        params: LimitOffsetPaginationParamDTO = Depends(),
        guard: AuthGuard = Security(
            auth.verify, scopes=["security:read:all"], use_cache=False
        ),
        security_usecase: SecurityUseCase = Depends(),
):
    securities_data, pagination = await security_usecase.list_security_data(
        limit=params.limit,
        offset=params.offset,
    )

    response = ApiResponse[list[SecurityDataSerializer]](
        data=securities_data,
        meta=MetaData(message=response_messages.fetch_success, pagination=pagination),
    )
    return response


@router.get(
    "/{security_id}",
    response_model=ApiResponse[SecurityDataSerializer],
    summary=crud_handler.fetch_summary,
    description=crud_handler.fetch_description,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_security_data(
        security_id: int,
        guard: AuthGuard = Security(
            auth.verify, scopes=["security:read"], use_cache=False
        ),
        security_usecase: SecurityUseCase = Depends(),
):
    security_data = await security_usecase.get_security_data(security_id)

    response = ApiResponse[SecurityDataSerializer](
        data=security_data,
        meta=MetaData(message=response_messages.fetch_success),
    )
    return response


@router.post(
    "/",
    response_model=ApiResponse[SecurityDataSerializer],
    summary=crud_handler.create_summary,
    description=crud_handler.create_description,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_security_data(
        security_data: SecurityDataCreateDto,
        guard: AuthGuard = Security(
            auth.verify, scopes=["security:write"], use_cache=False
        ),
        security_usecase: SecurityUseCase = Depends(),
):
    security_data = await security_usecase.create_security_data(security_data, user_id=guard.sub)

    response = ApiResponse[SecurityDataSerializer](
        data=security_data,
        meta=MetaData(message=response_messages.create_success),
    )
    return response


@router.put(
    "/{security_id}",
    response_model=ApiResponse[SecurityDataSerializer],
    summary=crud_handler.update_summary,
    description=crud_handler.update_description,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def update_security_data(
        security_id: str,
        security_data: SecurityDataUpdateDto,
        guard: AuthGuard = Security(
            auth.verify, scopes=["security:write"], use_cache=False
        ),
        security_usecase: SecurityUseCase = Depends(),
):
    security_data = await security_usecase.update_security_data(security_id, security_data)

    response = ApiResponse[SecurityDataSerializer](
        data=security_data,
        meta=MetaData(message=response_messages.update_success),
    )
    return response


@router.patch(
    "/{security_id}",
    response_model=ApiResponse[SecurityDataSerializer],
    summary=crud_handler.partial_update_summary,
    description=crud_handler.partial_update_description,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def partial_update_security_data(
        security_id: int,
        security_data: SecurityDataPartialUpdateDto,
        guard: AuthGuard = Security(
            auth.verify, scopes=["security:write"], use_cache=False
        ),
        security_usecase: SecurityUseCase = Depends(),
):
    security_data = await security_usecase.update_security_data(security_id, security_data)

    response = ApiResponse[SecurityDataSerializer](
        data=security_data,
        meta=MetaData(message=response_messages.update_success),
    )
    return response


@router.delete(
    "/{security_id}",
    response_model=None,
    summary=crud_handler.delete_summary,
    description=crud_handler.delete_description,
    status_code=status.HTTP_204_NO_CONTENT,
    response_model_exclude_none=True,
)
async def delete_security_data(
        security_id: int,
        guard: AuthGuard = Security(
            auth.verify, scopes=["security:delete"], use_cache=False
        ),
        security_usecase: SecurityUseCase = Depends(),
):
    await security_usecase.delete_security_data(security_id)

    return None
