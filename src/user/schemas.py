from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field, root_validator, validator

from src.auth.constants import AuthMethod, UserRole
from src.schemas import BaseModel
from src.utils import validate_strong_password


class UserData(BaseModel):
    id: UUID
    email: EmailStr
    password: bytes | None
    first_name: str | None
    last_name: str | None
    full_name: str | None
    styles: list[str] | None
    gender: str | None
    bust: int | None
    waist: int | None
    hip: int | None
    weight: float | None
    height: float | None
    role: UserRole
    is_active: bool
    is_activated: bool
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


class UserCreate(BaseModel):
    email: EmailStr
    password: str | None = Field(min_length=6, max_length=128)
    auth_method: AuthMethod | None = Field(default=None, hidden=True)
    first_name: str | None
    last_name: str | None

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not password:
            return password
        return validate_strong_password(password)


class UserUpdate(BaseModel):
    password: str | None
    first_name: str | None
    last_name: str | None
    gender: str | None
    styles: list[str] | None
    bust: int | None
    waist: int | None
    hip: int | None
    weight: float | None
    height: float | None

    @root_validator
    def validate_at_least_one_field_specified(cls, values):
        if all(v is None for v in values.values()):
            raise ValueError("At least one field must be provided!")
        return values

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if password is not None:
            return validate_strong_password(password)
        return None
