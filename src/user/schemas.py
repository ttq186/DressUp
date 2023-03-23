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
    styles: list[str] | None
    gender: str | None
    burst: int | None
    waist: int | None
    hip: int | None
    weight: float | None
    height: float | None
    is_admin: bool | None
    is_active: bool | None
    is_activated: bool | None
    auth_method: AuthMethod
    created_at: datetime | None
    updated_at: datetime | None

    @validator("full_name", always=True)
    def set_full_name(cls, v, values) -> str:
        return " ".join(
            value
            for value in [values.get("first_name"), values.get("last_name")]
            if value
        )


class UserOut(User):
    id: int
    email: EmailStr
    is_admin: bool
    is_active: bool
    is_activated: bool
    styles: list[str] | None


class UserIn(ORJSONModel):
    password: str | None
    first_name: str | None
    last_name: str | None
    gender: str | None
    styles: list[str] | None
    burst: int | None
    waist: int | None
    hip: int | None
    weight: float | None
    height: float | None

    @validator("password")
    def valid_password(cls, password: str) -> str:
        return validate_strong_password(password)
