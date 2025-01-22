from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SquareResult(BaseModel):
    original_value: int
    square_count: int
    squares: list[int]
    time_of_calculation: Decimal


class SquareResultList(SquareResult):
    id: int
    squares: str


class SquareResultDetailed(SquareResultList):
    created_at: datetime
    modified_at: datetime
