import json
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from database import SquareInfo


class SquareResult(BaseModel):
    original_value: int
    square_count: int
    squares: list[int]
    time_of_calculation: Decimal

    def get_db_model(self) -> SquareInfo:
        return SquareInfo(
            original_value=self.input_value,
            square_count=self.square_count,
            squares=json.dumps(self.squares),
            time_of_calculation=self.time_of_calculation
        )


class SquareResultList(SquareResult):
    id: int
    squares: str


class SquareResultDetailed(SquareResultList):
    created_at: datetime
    modified_at: datetime
