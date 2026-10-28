from typing import Any, ClassVar, Generic, TypeVar, cast

from sqlalchemy import delete, inspect as sa_inspect, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseDB

ModelT = TypeVar("ModelT", bound=BaseDB)


class BaseRepository(Generic[ModelT]):
    # Subclasses assign the ORM model at class level:
    #   class EmployeeRepository(BaseRepository[EmployeeDB]):
    #       _model = EmployeeDB
    #
    _model: ClassVar[type]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _pk(self) -> Any:
        # SQLAlchemy's inspect() returns the mapper for the class, which
        # exposes the underlying Table columns for the primary key.
        # Using the mapped Table column (not an InstrumentedAttribute) in a
        # WHERE clause works identically and does not require knowing the PK
        # attribute name ("id", "employee_id", etc.) at the base-class level.
        return sa_inspect(self._model).mapper.primary_key[0]

    async def get(self, pk: Any) -> ModelT | None:
        result = await self._session.execute(select(self._model).where(self._pk() == pk))
        return result.scalar_one_or_none()

    async def get_many(self, offset: int = 0, limit: int = 100) -> list[ModelT]:
        # Always paginate unbounded queries. A SELECT without LIMIT on a
        # production table can return millions of rows, saturate memory, and
        # time out the database connection pool.
        # ORDER BY is required by MSSQL whenever OFFSET/FETCH is used.
        result = await self._session.execute(select(self._model).order_by(self._pk()).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: dict) -> ModelT:
        instance = self._model(**data)
        self._session.add(instance)
        # flush() sends the INSERT to the database within the current
        # transaction without committing it. This is important for two reasons:
        # 1. The database assigns auto-generated values (identity, sequences,
        #    server defaults) and we need them back before returning.
        # 2. The service layer owns the commit boundary. flush() lets multiple
        #    repository calls participate in the same transaction before the
        #    service issues a single commit.
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def update(self, pk: Any, data: dict) -> ModelT | None:
        # Bulk UPDATE via execute() is more efficient than the ORM fetch-then-modify
        # pattern (which costs an extra SELECT). We issue the UPDATE, flush it
        # to apply within the transaction, then re-fetch so the caller always
        # receives a fresh, accurate model instance.
        await self._session.execute(update(self._model).where(self._pk() == pk).values(**data))
        await self._session.flush()
        return await self.get(pk)

    async def delete(self, pk: Any) -> bool:
        result = cast(CursorResult[Any], await self._session.execute(delete(self._model).where(self._pk() == pk)))
        # rowcount is the number of rows affected. Returning a bool lets the
        # service layer raise NotFoundException without knowing SQL details.
        return result.rowcount > 0

    async def exists(self, **filters: Any) -> bool:
        # .limit(1) short-circuits the query as soon as one matching row is
        # found — no need to count all matching rows.
        stmt = select(self._model).limit(1)
        for attr, value in filters.items():
            stmt = stmt.where(getattr(self._model, attr) == value)
        result = await self._session.execute(stmt)
        return result.first() is not None
