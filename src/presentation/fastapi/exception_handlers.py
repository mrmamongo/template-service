from collections.abc import Awaitable
from collections.abc import Callable
from typing import TypeVar

from fastapi import FastAPI
from jwcrypto.common import JWException
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.errors import BaseError
from src.application.errors import BaseErrorGroup

TError = TypeVar('TError', bound=BaseError)


async def _jwexception_error_handler(
    request: Request, error: JWException
) -> JSONResponse:
    logger.error(f'JWException: {error}')
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={'errors': [str(error)]}
    )


def _make_exception_handler(
    ex_type: type[TError],
) -> Callable[[Request, TError], Awaitable[JSONResponse]]:
    async def exception_handler(request: Request, exc: TError) -> JSONResponse:
        logger.error(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={'errors': [str(exc)]},
        )

    return exception_handler


async def _exception_group_handler(
    request: Request, exc: BaseErrorGroup
) -> JSONResponse:
    logger.error('Some errors...', errors=exc.exceptions)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'errors': [str(exc) for exc in exc.exceptions]},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков ошибок FastAPI."""
    for exc_type in [
        BaseError,
    ]:
        app.exception_handler(exc_type)(_make_exception_handler(exc_type))
    app.exception_handler(BaseErrorGroup)(_exception_group_handler)
    app.exception_handler(JWException)(_jwexception_error_handler)
