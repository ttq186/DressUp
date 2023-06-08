from uuid import UUID

from sqlalchemy import insert, select

from src.auth import security
from src.database import database
from src.user.schemas import (
    ContactCreate,
    ContactData,
    UserCreate,
    UserData,
    UserUpdate,
)
from src.user.table import contact_tb, user_tb


class UserRepo:
    async def create(self, create_data: UserCreate) -> UserData:
        if create_data.password:
            create_data.password = await security.hash_password(create_data.password)  # type: ignore
        insert_query = insert(user_tb).values(create_data.dict()).returning(user_tb)
        result = await database.fetch_one(insert_query)
        return UserData(**result._mapping)  # type: ignore

    async def get(self, id: UUID) -> UserData | None:
        select_query = select(user_tb).where(user_tb.c.id == id)
        result = await database.fetch_one(select_query)
        return UserData(**result._mapping) if result else None

    async def get_by_email(self, email: str) -> UserData | None:
        select_query = select(user_tb).where(user_tb.c.email == email)
        result = await database.fetch_one(select_query)
        return UserData(**result._mapping) if result else None

    async def update_user(self, id: UUID, update_data: UserUpdate | dict) -> UserData:
        if isinstance(update_data, UserUpdate):
            update_data = update_data.dict(exclude_unset=True, exclude_none=True)
        if "password" in update_data:
            update_data["password"] = await security.hash_password(
                update_data["password"]
            )
        update_query = (
            user_tb.update()
            .values(update_data)
            .where(user_tb.c.id == id)
            .returning(user_tb)
        )
        result = await database.fetch_one(update_query)
        return UserData(**result._mapping)  # type: ignore

    async def create_contact(self, create_data: ContactCreate) -> ContactData:
        insert_query = (
            insert(contact_tb).values(create_data.dict()).returning(contact_tb)
        )
        result = await database.fetch_one(insert_query)
        return ContactData(**result._mapping)  # type: ignore
