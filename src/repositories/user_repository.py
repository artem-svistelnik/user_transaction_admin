from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.user import User
from repositories.base import GenericRepository
from schemas.user_schemas import SignUpSchema


class UserRepository(GenericRepository[User]):

    async def create_user(self, user: SignUpSchema):
        user = await self.create(
            self.model(
                username=user.username,
            ),
            refresh=True,
        )
        return user

    async def get_user_by_id(self, id: int):
        query = (
            select(self.model)
            .where(self.model.id == id)
            .options(
                joinedload(self.model.transactions),
            )
        )
        results = await self._run_query(query)
        return results[0].unique().scalars().one()

    async def get_users(self):
        query = select(self.model).options(
            joinedload(self.model.transactions),
        )
        results = await self._run_query(query)
        return results[0].unique().scalars().all()
