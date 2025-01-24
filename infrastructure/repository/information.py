from sqlalchemy import select, Select
from sqlalchemy.ext.baked import Result

from database import SquareInfo
from infrastructure.repository.base import BaseRepository


class InformationRepository(BaseRepository):

    async def _get_by_id(self, unit_id: int) -> SquareInfo:
        info: SquareInfo | None = await self._session.get(SquareInfo, unit_id)
        return info

    def _get_all_select(self) -> Select:
        return select(SquareInfo).order_by(SquareInfo.id.desc())
