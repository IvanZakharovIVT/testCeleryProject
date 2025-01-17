from functools import cached_property

from infrastructure.enums.base_enum import DescribedEnum


class TaskStatus(str, DescribedEnum):
    CREATED = "created"  # Распознан
    SUCCESS = "success"  # Черновик
    ERROR = "error"  # Отправлен валютному агенту | Опубликован

    @cached_property
    def _description_items(self) -> dict:
        return {
            self.CREATED: 'Задача создана',
            self.SUCCESS: 'Задача успешно завершена',
            self.ERROR: 'Ошибка'
        }
