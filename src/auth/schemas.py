from pydantic import EmailStr, Field, validator

from src.schemas import ORJSONModel
from src.utils import validate_strong_password


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
    email: str
    is_admin: bool = False
    is_activated: bool
    is_active: bool


class AccessTokenResponse(ORJSONModel):
    access_token: str
    refresh_token: str


class UserEmail(ORJSONModel):
    email: EmailStr


class UserResetPassword(ORJSONModel):
    token: str
    new_password: str

    @validator("new_password")
    def valid_password(cls, new_password: str) -> str:
        return validate_strong_password(new_password)


class UserActivate(ORJSONModel):
    token: str
