import re
from datetime import datetime

from pydantic import EmailStr, Field, validator

from src.schemas import ORJSONModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


def validate_strong_password(password: str) -> str:
    if not re.match(STRONG_PASSWORD_PATTERN, password):
        raise ValueError(
            "Password must contain at least "
            "one lower character, "
            "one upper character, "
            "digit or "
            "special symbol"
        )

    return password


class AuthUser(ORJSONModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

    @validator("password")
    def valid_password(cls, password: str) -> str:
        return validate_strong_password(password)


class AuthUserViaGoogle(ORJSONModel):
    id_token: str


class JWTData(ORJSONModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(ORJSONModel):
    access_token: str
    refresh_token: str


class UserResponse(ORJSONModel):
    email: EmailStr


class UserEmail(ORJSONModel):
    email: EmailStr


class User(ORJSONModel):
    id: int
    email: EmailStr
    username: str | None
    is_admin: bool
    is_active: bool
    is_activated: bool
    auth_method: str
    created_at: datetime
    updated_at: datetime | None


class UserResetPassword(ORJSONModel):
    token: str
    new_password: str

    @validator("new_password")
    def valid_password(cls, new_password: str) -> str:
        return validate_strong_password(new_password)


class UserActivate(ORJSONModel):
    token: str
