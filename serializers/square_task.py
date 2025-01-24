from pydantic import BaseModel

from database import SquareCalculationTask
from infrastructure.enums.task_enum import TaskStatus


class SquareTaskCreate(BaseModel):
    input_value: int

    def get_db_model(self) -> SquareCalculationTask:
        return SquareCalculationTask(
            input_value=self.input_value,
        )


class SquareTaskGet(BaseModel):
    input_value: int
    status: TaskStatus
    error_message: str
