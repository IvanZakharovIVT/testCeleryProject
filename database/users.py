from sqlalchemy import Column, String

from database import BaseDBModel


class User(BaseDBModel):
    __tablename__ = 'users'

    username = Column(String(), index=True, unique=True)
    full_name = Column(String())
    user_type = Column(String(20))
    password = Column(String(255))
