# from typing import Sequence
#
# from fastapi import APIRouter, Depends, status
# from fastapi.security import HTTPBasicCredentials
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from database_conf.models import Fee
# from infrastructure.enums.user_type import UserType
# from infrastructure.helpers.user import authenticate_and_get_user_jwt, check_user_permissions
# from repository.fee import FeeRepository
# from repository.users import UserRepository
# from security import token_security
# from serializers.fee import FeeCreate, FeeDetail, FeeUpdate
#
# from config.db_config import get_session
#
# router = APIRouter(tags=['Fee'])
#
#
# @router.get(
#     '/user_fees',
#     summary='Получение всех комиссий пользователя по id',
#     description='Получение всех комиссий пользователя по id. Доступно только для админа',
#     response_model=Sequence[FeeDetail]
# )
# async def get_user_fees(
#         user_id: int,
#         session: AsyncSession = Depends(get_session),
#         credentials: HTTPBasicCredentials = Depends(token_security),
# ) -> Sequence[Fee]:
#     user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
#
#     await check_user_permissions(user, [UserType.admin])
#     fees: Sequence[Fee] = await FeeRepository(session).get_user_fees(user_id)
#     return fees
#
#
# @router.get(
#     '/fees',
#     summary='Получение всех комиссий',
#     description='Получение всех комиссий текущего авторизованного пользователя. Доступно только для рублёвого агента',
#     response_model=Sequence[FeeDetail]
# )
# async def get_all_fees(
#         session: AsyncSession = Depends(get_session),
#         credentials: HTTPBasicCredentials = Depends(token_security),
# ) -> Sequence[Fee]:
#     user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
#
#     await check_user_permissions(user, [UserType.ruble_agent, UserType.admin])
#
#     fees: Sequence[Fee] = await FeeRepository(session).get_user_fees(user.id)
#     return fees
#
#
# @router.post(
#     '/fees',
#     summary='Добавление новой комиссии',
#     description='Добавление новой комиссии для определенного пользователя. '
#                 'Добавить может только администратор. И только для рублевого агента',
#     status_code=201,
#     response_model=FeeDetail
# )
# async def add_fee(
#         new_fee: FeeCreate,
#         session: AsyncSession = Depends(get_session),
#         credentials: HTTPBasicCredentials = Depends(token_security),
# ) -> FeeDetail:
#     user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
#
#     await check_user_permissions(user, [UserType.admin])
#
#     target_user = await UserRepository(session).get_user_by_id(new_fee.user_id)
#     await check_user_permissions(target_user, [UserType.ruble_agent])
#
#     fee: Fee = await FeeRepository(session).add_fee(new_fee)
#
#     fee_response: FeeDetail = FeeDetail.from_orm(fee)
#     await session.commit()
#     return fee_response
#
#
# @router.patch(
#     '/fees/{fee_id}',
#     summary='Изменение комиссии',
#     description='Изменение комиссии для определенного пользователя. Доступно только для администратора',
#     status_code=status.HTTP_200_OK,
#     response_model=FeeUpdate
# )
# async def update_fee(
#         fee_id: int,
#         new_fee: FeeUpdate,
#         session: AsyncSession = Depends(get_session),
#         credentials: HTTPBasicCredentials = Depends(token_security),
# ):
#     user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
#
#     await check_user_permissions(user, [UserType.admin])
#
#     repo = FeeRepository(session)
#     await repo.update_fee(fee_id, new_fee)
#     await repo.commit()
#
#     return await repo.get_fee(fee_id)
#
#
# @router.delete(
#     '/fees/{fee_id}',
#     summary='Удаление комиссии',
#     description='Удаление комиссии. Доступно только для администратора',
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_fee(
#         fee_id: int,
#         session: AsyncSession = Depends(get_session),
#         credentials: HTTPBasicCredentials = Depends(token_security),
# ):
#     user = await authenticate_and_get_user_jwt(credentials.get('username'), session)
#
#     await check_user_permissions(user, [UserType.admin])
#
#     repo = FeeRepository(session)
#     await repo.delete_fee(fee_id)
#
#     await repo.commit()
