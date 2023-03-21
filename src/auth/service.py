import uuid
from datetime import datetime, timedelta

from databases.interfaces import Record
from pydantic import UUID4
from sqlalchemy import insert, select

from src import utils
from src.auth import jwt
from src.auth.config import auth_config
from src.auth.database import refresh_token_tb, user_tb
from src.auth.exceptions import (
    AccountNotActivated,
    AccountSuspended,
    InvalidCredentials,
)
from src.auth.schemas import AuthUser, User, UserActivate, UserResetPassword
from src.auth.security import check_password, hash_password
from src.auth.utils import send_activate_email, send_reset_password_email
from src.database import database


async def create_user(user: AuthUser) -> Record | None:
    insert_query = (
        insert(user_tb)
        .values(
            {
                "email": user.email,
                "password": hash_password(user.password),
            }
        )
        .returning(user_tb)
    )

    return await database.fetch_one(insert_query)


async def get_user_by_id(user_id: int) -> Record | None:
    select_query = select(user_tb).where(user_tb.c.id == user_id)
    return await database.fetch_one(select_query)


async def get_user_by_email(email: str) -> Record | None:
    select_query = select(user_tb).where(user_tb.c.email == email)
    return await database.fetch_one(select_query)


async def create_refresh_token(
    *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = refresh_token_tb.insert().values(
        uuid=uuid.uuid4(),
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await database.execute(insert_query)

    return refresh_token


async def get_refresh_token(refresh_token: str) -> Record | None:
    select_query = refresh_token_tb.select().where(
        refresh_token_tb.c.refresh_token == refresh_token
    )

    return await database.fetch_one(select_query)


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    update_query = (
        refresh_token_tb.update()
        .values(expires_at=datetime.utcnow() - timedelta(days=1))
        .where(refresh_token_tb.c.uuid == refresh_token_uuid)
    )

    await database.execute(update_query)


async def authenticate_user(auth_data: AuthUser) -> Record:
    user = await get_user_by_email(auth_data.email)
    if not user or not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    if not user["is_active"]:
        raise AccountSuspended()

    if not user["is_activated"]:
        raise AccountNotActivated()
    return user


def create_and_send_activate_email(user: User) -> None:
    username = user.username or user.email.split("@")[0]
    token = jwt.create_access_token(
        user=user.dict(),
        expires_delta=timedelta(minutes=15),
        secret_key=auth_config.JWT_EXTRA_SECRET,
    )
    activate_url = f"{auth_config.SITE_DOMAIN}/users/activate?token={token}"
    send_activate_email(
        receiver_email=user.email,
        username=username,
        activate_url=activate_url,
    )


def create_and_send_reset_password_email(user: User) -> None:
    username = user.username or user.email.split("@")[0]
    token = jwt.create_access_token(
        user=user.dict(),
        expires_delta=timedelta(minutes=10),
        secret_key=auth_config.JWT_EXTRA_SECRET,
    )
    reset_url = f"{auth_config.SITE_DOMAIN}/users/reset-password?token={token}"
    send_reset_password_email(
        receiver_email=user.email,
        username=username,
        reset_url=reset_url,
    )


async def reset_password(user_reset_payload: UserResetPassword) -> None:
    user_payload = jwt.decode_token(
        token=user_reset_payload.token, secret_key=auth_config.JWT_EXTRA_SECRET
    )
    update_query = (
        user_tb.update()
        .values(password=hash_password(user_reset_payload.new_password))
        .where(user_tb.c.email == user_payload["email"])
    )
    await database.fetch_one(update_query)


async def activate_account(user_activate_payload: UserActivate) -> None:
    user_payload = jwt.decode_token(
        token=user_activate_payload.token, secret_key=auth_config.JWT_EXTRA_SECRET
    )
    update_query = (
        user_tb.update()
        .values(is_activated=True)
        .where(user_tb.c.email == user_payload["email"])
    )
    await database.fetch_one(update_query)
