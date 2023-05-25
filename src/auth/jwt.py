from datetime import datetime, timedelta

from jose import JWTError, jwt

from src.auth.config import settings
from src.auth.exceptions import InvalidToken
from src.user.schemas import UserData


def create_access_token(
    user: UserData,
    expires_delta: timedelta = timedelta(seconds=settings.JWT_EXPIRES_SECONDS),
    secret_key: str = settings.JWT_SECRET,
) -> str:
    jwt_data = {
        "sub": user.email,
        "user_id": str(user.id),
        "exp": datetime.utcnow() + expires_delta,
        "role": user.role,
        "is_active": user.is_active,
        "is_activated": user.is_activated,
    }
    return jwt.encode(claims=jwt_data, key=secret_key, algorithm=settings.JWT_ALG)


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
