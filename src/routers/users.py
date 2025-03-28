from typing import Annotated

from fastapi.security import HTTPBasicCredentials

from src.infrastructure.enums.user_type import UserType
from src.infrastructure.helpers.user import authenticate_and_get_user_jwt, check_user_permissions, authenticate_and_get_user
from security import token_security, basic_security, access_security
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.infrastructure.repository.users import UserRepository
from src.serializers.square_task import SquareTaskGet

from src.config.db_config import get_session
from src.serializers.users import UserBase, UserCreateResponse
from src.services.user.create_user_service import CreateUserService

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
    return {"access_token": access_security.create_access_token(subject=subject)}



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
