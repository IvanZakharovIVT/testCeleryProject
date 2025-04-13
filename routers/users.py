from datetime import timedelta
from typing import Annotated

from fastapi.security import HTTPBasicCredentials

from config.settings import AUTH_TOKEN_TIMEDELTA, REFRESH_TOKEN_TIMEDELTA
from infrastructure.enums.user_type import UserType
from infrastructure.helpers.user import authenticate_and_get_user_jwt, check_user_permissions, authenticate_and_get_user
from security import token_security, basic_security, access_security, refresh_security, get_current_user
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from infrastructure.repository.users import UserRepository
from serializers.square_task import SquareTaskGet

from config.db_config import get_session
from serializers.users import UserBase, UserCreateResponse
from services.user.create_user_service import CreateUserService

router = APIRouter(tags=['users'])


@router.get(
    '/user/{user_id}',
    summary='Получение данных пользователя',
    description='Получение данных пользователя',
    response_model=SquareTaskGet
)
async def get_user_by_id(
        user_id: int,
        credentials: Annotated[dict, Depends(token_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
    await check_user_permissions(user, [UserType.ADMIN])
    return await UserRepository(session).get_by_id(user_id)


@router.post("/auth")
async def auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user(credentials.username, credentials.password, session)

    subject = {"username": user.username, "id": user.id, "user_type": user.user_type}
    return {
        "access_token": access_security.create_access_token(
            subject=subject,
            expires_delta=timedelta(minutes=AUTH_TOKEN_TIMEDELTA)
        ),
        "refresh_token": refresh_security.create_refresh_token(
            subject=subject,
            expires_delta=timedelta(minutes=REFRESH_TOKEN_TIMEDELTA)
        ),
    }

@router.post("/auth_cookie")
async def auth_cookie(
        response: Response,
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user(credentials.username, credentials.password, session)

    subject = {"username": user.username, "id": user.id, "user_type": user.user_type}
    auth_token = access_security.create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=AUTH_TOKEN_TIMEDELTA)
    )
    refresh_token_val = refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(minutes=REFRESH_TOKEN_TIMEDELTA)
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {auth_token}",
        httponly=True,
        max_age=AUTH_TOKEN_TIMEDELTA*60,  # 30 минут
        secure=True,  # Только для HTTPS
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token_val}",
        httponly=True,
        max_age=REFRESH_TOKEN_TIMEDELTA*60,  # 30 минут
        secure=True,  # Только для HTTPS
        samesite="lax"
    )
    return {"message": "Successfully logged in"}

@router.post("/refresh")
async def refresh_token(
    token: Annotated[dict, Depends(refresh_security)],
):
    return {
        "access_token": access_security.create_access_token(
            subject=token.subject,
            expires_delta = timedelta(minutes=AUTH_TOKEN_TIMEDELTA)
        )
    }


@router.post(
    '/create_user',
    summary='Создание пользователя',
    description='Создание пользователя',
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: UserBase,
        credentials: Annotated[dict, Depends(token_security)],
        session: AsyncSession = Depends(get_session),
):
    auth_user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
    await check_user_permissions(auth_user, [UserType.ADMIN])
    new_user: UserCreateResponse = await CreateUserService(session).create(user)
    await session.commit()
    return new_user

@router.get("/protected")
async def protected_route(request: Request, current_user: str = Depends(get_current_user)):
    # Доступно только с валидным токеном
    return {"message": "Protected data", "user": current_user}
