from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class GetSquareResult(BaseModel):
    original_value: int
    square_count: int
    squares: list[int]
    time_of_calculation: Decimal
