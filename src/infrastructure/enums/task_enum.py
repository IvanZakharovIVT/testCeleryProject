from functools import cached_property

from src.infrastructure.enums.base_enum import DescribedEnum


class TaskStatus(str, DescribedEnum):
    CREATED = "created"  # Создан
    SUCCESS = "success"  # Завершен
    TIMEOUT = "timeout"  # Завершен
    ERROR = "error"  # Отправлен валютному агенту | Опубликован

    @cached_property
    def _description_items(self) -> dict:
        return {
            self.CREATED: 'Задача создана',
            self.SUCCESS: 'Задача успешно завершена',
            self.TIMEOUT: 'Время исполнения истекло',
            self.ERROR: 'Ошибка'
        }
