from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import SquareCalculationTask
from infrastructure.repository.tasks import TaskRepository
from serializers.square_task import SquareTaskGet, SquareTaskCreate
from celery_task import add_new_task

from config.db_config import get_session

router = APIRouter(tags=['tasks'])


@router.get(
    '/square/{task_id}',
    summary='Получение данных по задаче',
    description='Получение данных по задаче',
    response_model=SquareTaskGet
)
async def get_square_task(
        task_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await TaskRepository(session).get_by_id(task_id)


@router.post(
    '/square',
    summary='Создание задачи',
    description='Создание задачи',
)
async def create_square_task(
        task_data: SquareTaskCreate,
        session: AsyncSession = Depends(get_session),
):
    task = SquareCalculationTask(
        input_value=task_data.input_value,
    )
    session.add(task)
    await session.flush()
    await session.commit()
    return task


@router.post(
    '/square_celery',
    summary='Создание задачи (celery)',
    description='Создание задачи (celery)',
)
async def create_square_task(
        task_data: SquareTaskCreate,
        session: AsyncSession = Depends(get_session),
):
    task_celery = add_new_task.delay(task_data.input_value)
    task = SquareCalculationTask(
        input_value=task_data.input_value,
        celery_task_id=task_celery.id,
    )
    session.add(task)
    await session.flush()
    await session.commit()
