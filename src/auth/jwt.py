from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.config import settings
from src.auth.exceptions import AuthorizationFailed, AuthRequired, InvalidToken
from src.auth.schemas import JWTData
from src.user.schemas import UserData


def create_access_token(
    user: UserData,
    expires_delta: timedelta = timedelta(seconds=settings.JWT_EXPIRES_SECONDS),
    secret_key: str = settings.JWT_SECRET,
) -> str:
    jwt_data = {
        "sub": user.email,
        "id": str(user.id),
        "exp": datetime.utcnow() + expires_delta,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        "is_activated": user.is_activated,
    }
    return jwt.encode(claims=jwt_data, key=secret_key, algorithm=settings.JWT_ALG)


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
    token: JWTData | None = Depends(valid_jwt_token_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(valid_jwt_token),
) -> JWTData:
    if not token.is_admin:
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(valid_jwt_token_optional),
) -> None:
    if token and token.is_admin:
        return

    raise AuthorizationFailed()


def decode_token(
    token: str,
    secret_key: str = settings.JWT_SECRET,
    algorithms: list[str] | str = [settings.JWT_ALG],
) -> dict:
    try:
        payload = jwt.decode(token=token, key=secret_key, algorithms=algorithms)
        return payload
    except JWTError:
        raise InvalidToken()
