from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field, validator

from src.schemas import BaseModel
from src.utils import validate_strong_password


class AuthData(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

    @validator("password")
    def valid_password(cls, password: str) -> str:
        return validate_strong_password(password)


class JWTData(BaseModel):
    id: UUID
    email: str = Field(alias="sub")
    is_admin: bool = False
    is_activated: bool
    is_active: bool


class RefreshTokenData(BaseModel):
    id: UUID
    user_id: UUID
    token: str
    expires_at: datetime
    created_at: datetime | None
    updated_at: datetime | None


class TokenData(BaseModel):
    access_token: str
    refresh_token: str


class UserResetPassword(BaseModel):
    token: str
    new_password: str

    @validator("new_password")
    def valid_password(cls, new_password: str) -> str:
        return validate_strong_password(new_password)


class RefreshTokenCreate(BaseModel):
    user_id: UUID = Field(default=None, hidden=True)
    token: str
    expires_at: datetime


class RefreshTokenUpdate(BaseModel):
    token: str | None
    expires_at: datetime | None
