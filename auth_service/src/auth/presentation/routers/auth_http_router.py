from fastapi import APIRouter
from fastapi import Depends
from src.auth.application.usecases.auth_usecase import AuthUseCase
from src.auth.presentation.dto.auth_dto import UserLoginDTO, UserCreateDTO

object_name = "Auth"

router = APIRouter(prefix="/auth", tags=[object_name])


@router.post(
    "/login",
    response_model=None
)
async def login(
        login_dto: UserLoginDTO,
        auth_usecase: AuthUseCase = Depends(),
):
    return await auth_usecase.login(login_dto.email, login_dto.password)


@router.post(
    "/register",
    response_model=None
)
async def register(
        user_dto: UserCreateDTO,
        auth_usecase: AuthUseCase = Depends(),
):
    return await auth_usecase.create_user(user_dto)
