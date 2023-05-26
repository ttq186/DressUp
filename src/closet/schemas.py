from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.product.schemas import ProductData
from src.schemas import BaseModel


class ClosetData(BaseModel):
    id: UUID
    owner_id: UUID
    owned_products: list[ProductData] = []
    public_products: list[ProductData] = []
    created_at: datetime | None
    updated_at: datetime | None


class ClosetCreate(BaseModel):
    owner_id: UUID | None = Field(default=None, hidden=True)
    product_ids: list[UUID] = []


class ClosetUpdate(BaseModel):
    added_product_ids: list[int] = []
    removed_product_ids: list[int] = []
