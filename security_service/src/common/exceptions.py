import os
from datetime import datetime

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from starlette.requests import Request

from .response import ApiResponse
from .response import MetaData


class ExceptionMiddleware:
    def __init__(self, app) -> None:
        self.app = app
        self.app.add_exception_handler(
            HTTPException, self.http_exception_handler)
        self.app.add_exception_handler(Exception, self.exception_handler)
        self.app.add_exception_handler(
            RequestValidationError, self.request_validation_exception_handler)

    @staticmethod
    async def http_exception_handler(request, exc):
        headers = getattr(exc, "headers", None)
        if not is_body_allowed_for_status_code(exc.status_code):
            return Response(status_code=exc.status_code, headers=headers)
        payload = ApiResponse[None](
            meta=MetaData(
                server_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                has_error=True,
                message=exc.detail,
            ),
            data=None,
        )
        response = JSONResponse(
            payload.model_dump(exclude_none=True), status_code=exc.status_code, headers=headers
        )
        return response

    @staticmethod
    async def exception_handler(request, exc):
        payload = ApiResponse[None](
            meta=MetaData(
                server_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                has_error=True,
                message="InternalError",
            ),
            data=None,
        )

        if os.environ.get("DEBUG", "1") == "1":
            payload.meta.message = str(exc)
        else:
            payload.meta.message = "InternalError"
        response = JSONResponse(payload.model_dump(
            exclude_none=True), status_code=500)
        return response

    @staticmethod
    async def request_validation_exception_handler(
            request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        payload = ApiResponse[None](
            meta=MetaData(
                server_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                has_error=True,
                message=str(jsonable_encoder(exc.errors())),
            ),
            data=None,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": payload.model_dump(exclude_none=True)},
        )
