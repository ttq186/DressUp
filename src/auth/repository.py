from uuid import UUID

from src.auth.schemas import RefreshTokenCreate, RefreshTokenData, RefreshTokenUpdate
from src.auth.table import refresh_token_tb
from src.database import database


class AuthRepo:
    async def create_refresh_token(
        self, create_data: RefreshTokenCreate
    ) -> RefreshTokenData:
        insert_query = (
            refresh_token_tb.insert()
            .values(**create_data.dict())
            .returning(refresh_token_tb)
        )
        result = await database.fetch_one(insert_query)
        return RefreshTokenData(**result._mapping)  # type: ignore

    async def get_refresh_token(self, refresh_token: str) -> RefreshTokenData | None:
        select_query = refresh_token_tb.select().where(
            refresh_token_tb.c.token == refresh_token
        )
        result = await database.fetch_one(select_query)
        return RefreshTokenData(**result._mapping) if result else None

    async def update_refresh_token(
        self, user_id: UUID, update_data: RefreshTokenUpdate
    ) -> RefreshTokenData:
        update_query = (
            refresh_token_tb.update()
            .values(update_data.dict(exclude_unset=True))
            .where(refresh_token_tb.c.user_id == user_id)
            .returning(refresh_token_tb)
        )
        result = await database.fetch_one(update_query)
        return RefreshTokenData(**result._mapping)  # type: ignore
