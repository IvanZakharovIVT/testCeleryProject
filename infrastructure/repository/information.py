from sqlalchemy import select, Select
from sqlalchemy.ext.baked import Result

from database import SquareInfo
from infrastructure.repository.base import BaseRepository


class InformationRepository(BaseRepository):

    async def _get_by_id(self, unit_id: int) -> SquareInfo:
        info: SquareInfo | None = await self._session.get(SquareInfo, unit_id)
        return info

    async def get_all(self):
        task_selection = select(SquareInfo)
        task_ordering = task_selection.order_by(SquareInfo.id.desc())
        result = await self._session.execute(select(SquareInfo).order_by(SquareInfo.id.desc()))
        # select_request = self._get_all_select()
        # result = await self._session.execute(select_request)
        return result.scalars().all()

    async def _get_all(self) -> Result:
        return await self._session.execute(
            select(SquareInfo).order_by(SquareInfo.id.desc())
        )

    def _get_all_select(self) -> Select:
        return select(SquareInfo).order_by(SquareInfo.id.desc())
