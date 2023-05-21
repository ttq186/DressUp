from fastapi import Body, Cookie, Depends

from src.auth.constants import AuthMethod
from src.auth.exceptions import EmailNotRegistered, EmailTaken, RefreshTokenNotValid
from src.auth.repository import AuthRepo
from src.auth.schemas import RefreshTokenData
from src.auth.service import AuthService
from src.user.repository import UserRepo
from src.user.schemas import UserCreate, UserData
from src.utils import utc_now


async def get_auth_service(
    auth_repo: AuthRepo = Depends(), user_repo: UserRepo = Depends()
) -> AuthService:
    return AuthService(auth_repo=auth_repo, user_repo=user_repo)


async def valid_user_email(
    email: str = Body(embed=True), user_repo: UserRepo = Depends()
) -> UserData:
    user = await user_repo.get_by_email(email)
    if not user:
        raise EmailNotRegistered()
    return user


async def valid_user_create(
    user_create: UserCreate, user_repo: UserRepo = Depends()
) -> UserCreate:
    if await user_repo.get_by_email(user_create.email):
        raise EmailTaken()
    user_create.auth_method = AuthMethod.NORMAL
    return user_create


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
    repo: AuthRepo = Depends(),
) -> RefreshTokenData:
    refresh_token_data = await repo.get_refresh_token(refresh_token)
    if not refresh_token_data or not _is_valid_refresh_token(refresh_token_data):
        raise RefreshTokenNotValid()

    return refresh_token_data


async def valid_refresh_token_user(
    refresh_token: RefreshTokenData = Depends(valid_refresh_token),
    user_repo: UserRepo = Depends(),
) -> UserData:
    user = await user_repo.get(refresh_token.user_id)
    if not user:
        raise RefreshTokenNotValid()
    return user


def _is_valid_refresh_token(refresh_token: RefreshTokenData) -> bool:
    return utc_now() <= refresh_token.expires_at
