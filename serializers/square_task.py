from pydantic import BaseModel

from infrastructure.enums.task_enum import TaskStatus


class CreateSquareTask(BaseModel):
    input_value: int


class GetSquareTask(BaseModel):
    input_value: int
    status: TaskStatus
    error_message: str
