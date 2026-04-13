from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

import logging

from app.core.exceptions import (
    ValidationError,
    AlreadyExistsError,
    DatabaseError,
    NotFoundError,
)

logger = logging.getLogger(__name__)


async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


async def already_exists_handler(request: Request, exc: AlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


async def validation_fastapi_error_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error = errors[0]
    field = error.get("loc")[-1]
    msg = error.get("msg")
    
    return JSONResponse(
        status_code=422,
        content={"detail": f"Error in input field '{field}': {msg}"}
    )


async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


async def generic_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(AlreadyExistsError, already_exists_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(DatabaseError, database_error_handler)
    app.add_exception_handler(Exception, generic_handler)
    app.add_exception_handler(RequestValidationError, validation_fastapi_error_handler)