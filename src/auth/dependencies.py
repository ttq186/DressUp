from fastapi import Body, Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.config import settings
from src.auth.constants import AuthMethod
from src.auth.exceptions import (
    AuthRequired,
    EmailNotRegistered,
    EmailTaken,
    InvalidToken,
    RefreshTokenNotValid,
)
from src.auth.repository import AuthRepo
from src.auth.schemas import AuthData, JWTData, RefreshTokenData
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


async def valid_jwt_token_optional(
    token: str = Depends(
        OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)
    ),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def valid_jwt_token(
    jwt_data: JWTData | None = Depends(valid_jwt_token_optional),
) -> JWTData:
    if not jwt_data:
        raise AuthRequired()

    return jwt_data


async def valid_user(
    jwt_data: JWTData = Depends(valid_jwt_token),
    user_repo: UserRepo = Depends(),
) -> UserData:
    user = await user_repo.get(id=jwt_data.user_id)
    if not user:
        raise InvalidToken()
    return user


async def valid_user_create(
    auth_data: AuthData, user_repo: UserRepo = Depends()
) -> UserCreate:
    if await user_repo.get_by_email(auth_data.email):
        raise EmailTaken()
    return UserCreate(**auth_data.dict(), auth_method=AuthMethod.NORMAL)  # type: ignore


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
