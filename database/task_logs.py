from sqlalchemy import Column, Integer

from database.base import BaseDBModel


class TaskLogs(BaseDBModel):
    __tablename__ = 'calculation_count_logs'
    calculation_count = Column(Integer)
