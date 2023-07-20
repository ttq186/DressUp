from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, validator

from src.auth.constants import AuthMethod
from src.schemas import BaseModel
from src.user.constants import SubscriptionType


class AdminUserData(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str | None
    last_name: str | None
    full_name: str | None
    avatar_url: str | None
    is_active: bool | None
    is_activated: bool
    total_paid_amount: int
    subscription_type: SubscriptionType
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
