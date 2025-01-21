from sqlalchemy import Column, Integer, Numeric, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from database.base import BaseDBModel


class SquareInfo(BaseDBModel):
    __tablename__ = 'square_info'
    original_value = Column(BigInteger)
    square_count = Column(Integer)
    squares = Column(JSONB)
    time_of_calculation = Column(Numeric)
    recognition_tasks = relationship("SquareCalculationTask", back_populates="square_info", lazy="subquery")
