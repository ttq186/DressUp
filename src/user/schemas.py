from datetime import datetime

from pydantic import EmailStr, validator

from src.auth.constants import AuthMethod
from src.schemas import ORJSONModel
from src.utils import validate_strong_password


class User(ORJSONModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    full_name: str | None
    gender: str | None
    is_admin: bool | None
    is_active: bool | None
    is_activated: bool | None
    auth_method: AuthMethod
    created_at: datetime
    updated_at: datetime

    @validator("full_name", always=True)
    def set_full_name(cls, v, values) -> str:
        return " ".join(
            value for value in [values["first_name"], values["last_name"]] if value
        )


class UserOut(User):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    is_active: bool
    is_activated: bool


class UserIn(ORJSONModel):
    password: str | None
    first_name: str | None
    last_name: str | None
    gender: str | None

    @validator("password")
    def valid_password(cls, password: str) -> str:
        return validate_strong_password(password)
