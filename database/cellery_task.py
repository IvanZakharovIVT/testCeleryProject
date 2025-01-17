from sqlalchemy import Column, String, BigInteger

from database.base import BaseDBModel
from infrastructure.enums.task_enum import TaskStatus


class SquareCalculationTask(BaseDBModel):
    __tablename__ = 'square_calculation_task'
    input_value = Column(BigInteger)
    status = Column(String(16), nullable=False, default=TaskStatus.CREATED)
    error_message = Column(String())
