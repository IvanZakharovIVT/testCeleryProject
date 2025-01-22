from sqlalchemy import select
from sqlalchemy.ext.baked import Result

from database import SquareCalculationTask
from infrastructure.repository.base import BaseRepository


class TaskRepository(BaseRepository):

    async def _get_by_id(self, unit_id: int) -> SquareCalculationTask:
        info: SquareCalculationTask | None = await self._session.get(SquareCalculationTask, unit_id)
        return info

    async def _get_all(self) -> Result:
        return await self._session.execute(
            select(SquareCalculationTask).order_by(SquareCalculationTask.id.desc())
        )
