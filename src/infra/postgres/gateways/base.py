from typing import TypeVar

from adaptix import Retort
from sqlalchemy import Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.errors import DatabaseError
from src.application.errors import NotFoundError

TSchema = TypeVar('TSchema')


class BasePostgresGateway:
    def __init__(self, retort: Retort, session: AsyncSession, table: Table) -> None:
        self.retort = retort
        self.session = session
        self.table = table

    async def delete_by_id(self, entity_id: int | str) -> int | str:
        """Удаляет сущность по id."""
        stmt = self.table.delete().where(self.table.c.id == entity_id)

        try:
            result = await self.session.execute(stmt)
            if result.rowcount != 1:
                raise NotFoundError(model_name='chat')

            return entity_id
        except IntegrityError as e:
            raise DatabaseError(message=str(e)) from e
