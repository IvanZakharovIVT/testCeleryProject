from typing import Protocol

from database import BaseDBModel


class DBProtocol(Protocol):
    def get_db_model(self) -> BaseDBModel:
        pass