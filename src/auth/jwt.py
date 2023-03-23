from datetime import datetime, timedelta

from databases.interfaces import Record
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.config import auth_config
from src.auth.exceptions import AuthorizationFailed, AuthRequired, InvalidToken
from src.auth.schemas import JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)


def create_access_token(
    *,
    user: Record | dict,
    expires_delta: timedelta = timedelta(minutes=120),
    secret_key: str = auth_config.JWT_SECRET,
) -> str:
    jwt_data = {
        "sub": str(user["id"]),
        "exp": datetime.utcnow() + expires_delta,
        "email": str(user["email"]),
        "is_admin": user["is_admin"],
        "is_active": user["is_active"],
        "is_activated": user["is_activated"],
    }

    return jwt.encode(claims=jwt_data, key=secret_key, algorithm=auth_config.JWT_ALG)


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(parse_jwt_user_data),
) -> JWTData:
    if not token.is_admin:
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> None:
    if token and token.is_admin:
        return

    raise AuthorizationFailed()


def decode_token(
    token: str,
    secret_key: str = auth_config.JWT_SECRET,
    algorithms: list[str] | str = [auth_config.JWT_ALG],
) -> dict:
    try:
        payload = jwt.decode(token=token, key=secret_key, algorithms=algorithms)
        return payload
    except JWTError:
        raise InvalidToken()
