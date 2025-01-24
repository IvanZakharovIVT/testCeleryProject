from functools import cached_property

from infrastructure.enums.base_enum import DescribedEnum


class UserType(str, DescribedEnum):
    VIEWER = "viewer",
    CREATOR = "creator",
    ADMIN = "admin"

    @cached_property
    def _description_items(self) -> dict:
        return {
            self.VIEWER: 'Наблюдатель',
            self.CREATOR: 'Создатель записей',
            self.ADMIN: 'Администратор',
        }
