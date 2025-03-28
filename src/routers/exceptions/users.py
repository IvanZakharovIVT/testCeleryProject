from fastapi import FastAPI, HTTPException, Request
from starlette import status

from src.infrastructure.exceptions.user import UserAuthorizationError


async def user_authorization_error_exception_handler(
        request: Request,
        exc: UserAuthorizationError,
) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.error_message
    )


def setup_user_handlers(app: FastAPI):
    app.add_exception_handler(UserAuthorizationError, user_authorization_error_exception_handler)
