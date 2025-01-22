from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from database import SquareInfo
from database.base import BaseDBModel
from infrastructure.enums.task_enum import TaskStatus


class SquareCalculationTask(BaseDBModel):
    __tablename__ = 'square_calculation_task'
    input_value = Column(BigInteger)
    celery_task_id = Column(String)
    status = Column(String(16), nullable=False, default=TaskStatus.CREATED)
    error_message = Column(String())
    square_info_id = Column(ForeignKey(SquareInfo.id, ondelete="SET NULL"), nullable=True)

    square_info = relationship("SquareInfo", back_populates="recognition_tasks")
