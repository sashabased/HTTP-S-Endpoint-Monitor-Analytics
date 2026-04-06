from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ValidationError,
    AlreadyExistsError,
    DatabaseError,
    NotFoundError,
)


def register_exception_handler(app = FastAPI()):

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc) or "Resource not found"},
        )
    

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc) or "Already exists"},
        )
    

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc) or "Validation error"},
        )
    

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc) or "Internal database error"},
        )
    

    @app.exception_handler(Exception)
    async def generic_handler(reuquest: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )