from uuid import UUID

from src.user.repository import UserRepo
from src.user.schemas import (
    ContactCreate,
    ContactData,
    UserCreate,
    UserData,
    UserUpdate,
)


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def create_user(self, create_data: UserCreate) -> UserData:
        return await self.user_repo.create(create_data=create_data)

    async def update_user(self, user: UserData, update_data: UserUpdate) -> UserData:
        return await self.user_repo.update_user(id=user.id, update_data=update_data)

    async def create_contact(
        self, user_id: UUID, create_data: ContactCreate
    ) -> ContactData:
        create_data.user_id = user_id
        return await self.user_repo.create_contact(create_data=create_data)
