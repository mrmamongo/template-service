from collections.abc import Callable

from sqlalchemy import UnaryExpression
from sqlalchemy import asc
from sqlalchemy import desc

from src.application.enums.base import BaseENUM


class OrderEnum(BaseENUM):
    DESC = 'DESC'
    ASC = 'ASC'

    @property
    def sql(self) -> Callable[..., UnaryExpression]:
        """Метод возвращает направление сортировки для sqlalchemy.

        Returns:
            функции asc или desc
        """
        match self:
            case OrderEnum.ASC:
                return asc
            case OrderEnum.DESC:
                return desc
            case _:
                raise ValueError(f'Неизвестное значение {self}')
