from typing import Sequence, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.enums.user_type import UserType
from src.infrastructure.helpers.user import authenticate_and_get_user_jwt, check_user_permissions
from src.infrastructure.repository.information import InformationRepository
from security import token_security, access_security
from src.serializers.square_calc import SquareResultDetailed, SquareResultList

from src.config.db_config import get_session

router = APIRouter(tags=['calculation'])


@router.get(
    '/square_info/{info_id}',
    summary='Получение детальных данных по расчету квадратов',
    description='Получение детальных данных по расчету квадратов',
    response_model=SquareResultDetailed
)
async def get_square_result_by_id(
        credentials: Annotated[dict, Depends(token_security)],
        info_id: int,
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
    await check_user_permissions(user, [UserType.CREATOR, UserType.ADMIN, UserType.VIEWER])
    return await InformationRepository(session).get_by_id(info_id)


@router.get(
    '/square_info',
    summary='Получение данных по расчету квадратов',
    description='Получение данных по расчету квадратов',
    response_model=Sequence[SquareResultList]
)
async def get_square_results(
        credentials: Annotated[dict, Depends(token_security)],
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
    await check_user_permissions(user, [UserType.CREATOR, UserType.ADMIN, UserType.VIEWER])
    return await InformationRepository(session).get_all()


# @router.get(
#     '/square_info',
#     summary='Получение данных по расчету квадратов',
#     description='Получение данных по расчету квадратов',
#     response_model=Sequence[SquareResultList]
# )
# async def get_square_results(
#         token: Annotated[dict, Depends(access_security)],
#         session: AsyncSession = Depends(get_session),
# ):
#     credentials = token.subject
#     user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
#     await check_user_permissions(user, [UserType.CREATOR, UserType.ADMIN, UserType.VIEWER])
#     return await InformationRepository(session).get_all()
