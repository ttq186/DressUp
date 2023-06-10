from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import Field

from src.payment.constants import PaymentStatus
from src.schemas import BaseModel


class PaymentCreate(BaseModel):
    user_id: UUID | None = Field(hidden=True)
    subscription_id: Literal[2, 3]
    price: int


class PaymentData(BaseModel):
    user_id: UUID
    status: PaymentStatus
    subscription_id: int
    price: int
    created_at: datetime | None
