from datetime import datetime
from uuid import UUID

from src.schemas import BaseModel


class ProductData(BaseModel):
    id: UUID
    name: str
    description: str
    brand: str | None
    is_public: bool
    shopee_affiliate_url: str
    lazada_affiliate_url: str
    tiktok_affiliate_url: str
    image_urls: list[str]
    created_at: datetime | None
    updated_at: datetime | None


class ProductCreate(BaseModel):
    pass


class ProductUpdate(BaseModel):
    pass
