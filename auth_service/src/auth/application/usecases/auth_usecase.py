from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.auth.domain.services.repositories.auth_repository import UserSqlRepository
from src.auth.inferastractor.settings import settings
from src.auth.presentation.dto.auth_dto import UserCreateDTO
from passlib.context import CryptContext

from src.auth.presentation.serializers.auth_serializer import AuthPayload, TokenResponseSerializer
from datetime import datetime, timedelta, timezone
import jwt


class AuthUseCase:
    def __init__(self, user_repository: UserSqlRepository = Depends()):
        self.auth_service = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_email(self, email: str):
        user = await self.auth_service.get_user_by_email(email)
        if not user:
            return HTTPException(
                status_code=404, detail="User not found"
            )

        return user

    async def create_user(self, user: UserCreateDTO):
        user.password = self.pwd_context.hash(user.password)
        try:
            user = await self.auth_service.create_user(user)
            return await self.create_access_token(user.id)
        except IntegrityError:
            return HTTPException(
                status_code=400, detail="User already exists"
            )

    async def _verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, email: str, password: str):
        user = await self.auth_service.get_user_by_email(email)
        if not user:
            return False
        if not self._verify_password(password, user.password):
            return False
        return user

    async def create_access_token(self, id: int) -> TokenResponseSerializer:
        auth = AuthPayload(sub=id,
                           permissions=["me", "security:read",
                                        "security:write",
                                        "security:delete",
                                        "security:read:all"],
                           exp=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                           iat=datetime.now(timezone.utc)
                           )
        # encode
        token = jwt.encode(auth.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return TokenResponseSerializer(access_token=token,
                                       token_type="bearer",
                                       expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    async def login(self, email: str, password: str):
        user = await self.authenticate_user(email, password)
        if not user:
            return HTTPException(
                status_code=404, detail="User not found"
            )
        return await self.create_access_token(id=user.id)
