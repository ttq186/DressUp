from databases.interfaces import Record
from sqlalchemy import select

from src.auth.security import hash_password
from src.database import database
from src.user.database import user_tb
from src.user.schemas import UserIn


async def get_user_by_id(user_id: int) -> Record | None:
    select_query = select(user_tb).where(user_tb.c.id == user_id)
    return await database.fetch_one(select_query)


async def update_user(email: str, user_in: UserIn) -> None:
    update_values = user_in.dict(exclude_unset=True)
    if user_in.password:
        update_values["password"] = hash_password(user_in.password)
    update_query = (
        user_tb.update().values(update_values).where(user_tb.c.email == email)
    )
    return await database.execute(update_query)
