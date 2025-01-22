from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repository.information import InformationRepository
from serializers.square_calc import SquareResultDetailed, SquareResultList

from config.db_config import get_session

router = APIRouter(tags=['calculation'])


@router.get(
    '/square_info/{info_id}',
    summary='Получение детальных данных по расчету квадратов',
    description='Получение детальных данных по расчету квадратов',
    response_model=SquareResultDetailed
)
async def get_square_task(
        info_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await InformationRepository(session).get_by_id(info_id)


@router.get(
    '/square_info',
    summary='Получение данных по расчету квадратов',
    description='Получение данных по расчету квадратов',
    response_model=Sequence[SquareResultList]
)
async def get_square_task(
        session: AsyncSession = Depends(get_session),
):
    return await InformationRepository(session).get_all()
