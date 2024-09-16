import asyncio
from typing import Generic, Type, TypeVar, get_args

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import Base
from exceptions.base import DataConflictError, MultipleResultsError, NotFoundError

ModelT = TypeVar("ModelT", bound=Base)


class GenericRepository(Generic[ModelT]):
    model: Type[ModelT]
    primary_key: str = "id"
    _s: AsyncSession

    def __init__(self):
        self.model = get_args(self.__orig_bases__[0])[0]  # type: ignore

    def set_session(self, session):
        self._s = session

    async def _run_query(self, *queries, commit=False) -> list:
        tasks = []
        for query in queries:
            tasks.append(asyncio.create_task(self._s.execute(query)))
        response = await asyncio.gather(*tasks)
        if commit:
            await self._s.flush()
        return response  # type: ignore

    def _count_query(self, *filters):
        return select(func.count(getattr(self.model, self.primary_key))).where(*filters)

    @staticmethod
    def _get_results(data, joined=False):
        if joined:
            return data.scalars().unique().all()
        return data.scalars().all()

    async def get(self, pk) -> ModelT:
        results = await self._run_query(
            select(self.model).where(getattr(self.model, self.primary_key) == pk)
        )
        try:
            return results[0].unique().scalars().one()
        except NoResultFound as e:
            raise NotFoundError() from e
        except MultipleResultsFound as e:
            raise MultipleResultsError() from e

    async def create(self, model: ModelT, refresh=False) -> ModelT | None:
        try:
            self._s.add(model)
            await self._s.flush()
        except IntegrityError as e:
            raise DataConflictError() from e
        if refresh:
            await self._s.refresh(model)
            return model

    async def update_where(self, *filters, **fields) -> int:
        cnt = await self._run_query(update(self.model).where(*filters).values(**fields))
        self._s.expire_all()
        return cnt[0]

    async def update(self, model: ModelT, refresh=False) -> ModelT | None:
        try:
            self._s.add(model)
            await self._s.flush()
        except IntegrityError as e:
            raise DataConflictError() from e
        if refresh:
            await self._s.refresh(model)
            return model

    async def delete(self, model: ModelT):
        await self._s.delete(model)
        await self._s.flush()

    async def delete_where(self, *filters) -> int:
        results = await self._run_query(delete(self.model).where(*filters), commit=True)
        self._s.expire_all()
        return results[0]
