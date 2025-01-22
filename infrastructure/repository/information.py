from sqlalchemy import select
from sqlalchemy.ext.baked import Result

from database import SquareInfo
from infrastructure.repository.base import BaseRepository


class InformationRepository(BaseRepository):

    async def _get_by_id(self, unit_id: int) -> SquareInfo:
        info: SquareInfo | None = await self._session.get(SquareInfo, unit_id)
        return info

    async def _get_all(self) -> Result:
        return await self._session.execute(
            select(SquareInfo).order_by(SquareInfo.id.desc())
        )
