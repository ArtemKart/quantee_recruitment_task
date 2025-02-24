from typing import Callable

from fastapi import Request
from starlette.responses import JSONResponse

from app.exceptions.exceptions import BaseApiException


def create_exception_handler(
    status_code: int, detail: str
) -> Callable[[Request, BaseApiException], JSONResponse]:
    async def app_exception_handler(_: Request, exc: BaseApiException) -> JSONResponse:
        if exc.detail:
            content["message"] = exc.detail
        return JSONResponse(status_code=status_code, content=content)

    content = {"message": detail}
    return app_exception_handler
