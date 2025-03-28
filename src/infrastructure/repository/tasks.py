from sqlalchemy import select, Select

from database import SquareCalculationTask
from src.infrastructure.repository.base import BaseRepository


class TaskRepository(BaseRepository):

    async def _get_by_id(self, unit_id: int) -> SquareCalculationTask:
        info: SquareCalculationTask | None = await self._session.get(SquareCalculationTask, unit_id)
        return info

    def _get_all_select(self) -> Select:
        return select(SquareCalculationTask).order_by(SquareCalculationTask.id.desc())
