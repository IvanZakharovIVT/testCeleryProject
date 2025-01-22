from pydantic import BaseModel

from infrastructure.enums.task_enum import TaskStatus


class SquareTaskCreate(BaseModel):
    input_value: int


class SquareTaskGet(BaseModel):
    input_value: int
    status: TaskStatus
    error_message: str
