import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import Result, Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from celery_task import app as celery_app

from config.db_config import get_session
from config.settings import MAX_TASK_EXECUTION_TIME
from database import SquareCalculationTask, SquareInfo
from infrastructure.enums.task_enum import TaskStatus
from serializers.square_calc import GetSquareResult

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


async def schedule_worker(db_session: AsyncSession):
    while True:
        expired_time = datetime.now() - timedelta(seconds=MAX_TASK_EXECUTION_TIME)
        stmt = (
            update(SquareCalculationTask)
            .where(SquareCalculationTask.status == TaskStatus.CREATED.value,
                   SquareCalculationTask.created_at < expired_time)
            .values(status=TaskStatus.TIMEOUT.value)
        )
        await db_session.execute(stmt)
        await db_session.flush()

        query: Select = select(SquareCalculationTask).filter(
            SquareCalculationTask.status == TaskStatus.CREATED,
        )
        result: Result = await db_session.execute(query)
        tasks: Sequence[SquareCalculationTask] = result.scalars().all()
        for task in tasks:
            c_task = celery_app.AsyncResult(task.celery_task_id)
            if c_task.status == "SUCCESS":
                task_result = GetSquareResult(**json.loads(c_task.get()))
                new_info = SquareInfo(
                    original_value=task.input_value,
                    square_count=task_result.square_count,
                    squares=json.dumps(task_result.squares),
                    time_of_calculation=task_result.time_of_calculation
                )
                db_session.add(new_info)
                await db_session.flush()
                task.square_info_id = new_info.id
                task.status = TaskStatus.SUCCESS
                db_session.add(task)

        await db_session.commit()
        await asyncio.sleep(10)


async def main():
    async for db_session in get_session():
        await schedule_worker(db_session)


if __name__ == '__main__':
    asyncio.run(main())
