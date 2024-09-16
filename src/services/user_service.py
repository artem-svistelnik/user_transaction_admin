from repositories.user_repository import UserRepository
from schemas.user_schemas import SignUpSchema
from services.base import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def create_user(self, user: SignUpSchema):
        return await self.user_repo.create_user(user)

    async def get_users(self):
        return await self.user_repo.get_users()

    async def get_user(self, pk):
        return await self.user_repo.get_user_by_id(pk)

