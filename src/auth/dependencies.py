from datetime import datetime

from databases.interfaces import Record
from fastapi import Cookie, Depends

from src.auth import service
from src.auth.constants import AuthMethod
from src.auth.exceptions import (
    AccountCreatedByNormalMethod,
    AccountCreatedViaThirdParty,
    EmailNotRegistered,
    EmailTaken,
    RefreshTokenNotValid,
)
from src.auth.schemas import AuthUser, User, UserEmail


async def valid_user(user_email: UserEmail) -> User:
    user = await service.get_user_by_email(user_email.email)
    if not user:
        raise EmailNotRegistered()
    return User(**user._mapping)


async def valid_user_create(auth_user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(auth_user.email):
        raise EmailTaken()
    return auth_user


async def valid_normal_user_create(
    auth_user: AuthUser = Depends(valid_user_create),
) -> AuthUser:
    user = await service.get_user_by_email(auth_user.email)
    if user:
        if user["auth_method"] != AuthMethod.NORMAL:
            raise AccountCreatedViaThirdParty()
        raise EmailTaken()
    return auth_user


async def valid_oauth_user_create(
    auth_user: AuthUser = Depends(valid_user_create),
) -> AuthUser:
    user = await service.get_user_by_email(auth_user.email)
    if user:
        if user["auth_method"] == AuthMethod.NORMAL:
            raise AccountCreatedByNormalMethod()
        raise EmailTaken()
    return auth_user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> Record:
    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: Record = Depends(valid_refresh_token),
) -> Record:
    user = await service.get_user_by_id(refresh_token["user_id"])
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: Record) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
