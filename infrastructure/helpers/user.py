from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from infrastructure.enums.user_type import UserType
from infrastructure.exceptions.user import UserAuthorizationError
from infrastructure.repository.users import UserRepository
from security import token_security


async def authenticate_and_get_user(credentials: Annotated[HTTPBasicCredentials, Depends(token_security)],
                                    session: AsyncSession):
    user = await UserRepository(session).authenticate_user(credentials.username, credentials.password)

    return user


async def authenticate_and_get_user_jwt(username: str, session: AsyncSession):
    user = await UserRepository(session).get_user_by_username(username)
    if not user:
        raise UserAuthorizationError(username)

    return user


async def check_user_permissions(user: User, allowed_user_types: list[UserType]):
    if user.user_type not in allowed_user_types:
        allowed_roles = ', '.join([v.description for v in allowed_user_types])
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Недостаточно прав. Доступно только для {allowed_roles}")
