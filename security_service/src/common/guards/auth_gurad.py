from typing import List
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from src.common.logger import logger
from src.common.settings import settings
from src.common.serializer.auth_serializer import AuthPayload


class AuthGuard:
    def __init__(
            self,
    ):
        self.secret_key = settings.SECRET_KEY

    async def decode(self, token: str) -> AuthPayload:
        """Decodes the JWT token without verifying the signature (for placeholder purposes)"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"],
            )

        except jwt.PyJWTError as e:
            logger.error(f"Error decoding token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
            )
        try:
            auth_payload = AuthPayload(**payload)

        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
            )
        return auth_payload

    async def verify(
            self,
            security_scopes: SecurityScopes,
            token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ) -> AuthPayload:
        """Verifies the JWT token and checks required security scopes"""
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing"
            )

        payload = await self.decode(token.credentials)

        if security_scopes.scopes:
            self._check_claims(payload, "permissions", security_scopes.scopes)
        return payload

    @staticmethod
    def _check_claims(payload: AuthPayload, claim_name: str, expected_value: List[str]):
        """Checks the required claims in the token payload"""
        if claim_name not in payload.dict():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'No claim "{claim_name}" found in token',
            )

        payload_claim = payload.dict().get(claim_name)

        if claim_name == "scope":
            payload_claim = payload_claim.split(" ")

        if not any(scope in payload_claim for scope in expected_value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Missing required "{claim_name}" scope',
            )
