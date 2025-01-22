from typing import Sequence

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import SquareInfo
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
    info: SquareInfo | None = await session.get(SquareInfo, info_id)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # detail=exc.error_message
        )
    return info


@router.get(
    '/square_info',
    summary='Получение данных по расчету квадратов',
    description='Получение данных по расчету квадратов',
    response_model=Sequence[SquareResultList]
)
async def get_square_task(
        session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(SquareInfo).order_by(SquareInfo.id.desc())
    )
    return result.scalars().all()
