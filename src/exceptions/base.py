from fastapi import status
from sqlalchemy.exc import NoResultFound
from starlette.requests import Request
from starlette.responses import JSONResponse


class ApiError(Exception):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Not found"

    def __init__(self, detail: str = None, status_code: int = None):
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code

    def __str__(self):
        return f"{self.status_code}: {self.detail}"


async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def include_exception_handlers(app):
    @app.exception_handler(NoResultFound)
    async def err_404(request: Request, exc: NoResultFound):
        status_code = 404
        return JSONResponse(
            status_code=status_code,
            content={
                "status": status_code,
                "errorCode": "NOT_FOUND",
                "message": "Your are looking for something that does not exist.",
            },
        )


class DataConflictError(ApiError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Data conflict error"


class MultipleResultsError(ApiError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Multiple results found when only one expected"


class NotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"
