from datetime import datetime
from uuid import UUID

from src.schemas import BaseModel


class ProductData(BaseModel):
    id: int
    owner_id: UUID
    name: str
    description: str
    categories: list[str]
    brand: str | None
    material: str | None
    style: str | None
    pattern: str | None
    my_rating_score: float | None
    original_url: str
    transparent_background_image: str | None
    is_public: bool
    shopee_affiliate_url: str | None
    lazada_affiliate_url: str | None
    tiktok_affiliate_url: str | None
    image_urls: list[str]
    created_at: datetime | None
    updated_at: datetime | None


class ProductDatas(BaseModel):
    products: list[ProductData]
    total_rows: int


class ProductCreate(BaseModel):
    pass


class ProductUpdate(BaseModel):
    pass


class ProductRatingData(BaseModel):
    user_id: UUID
    product_id: int
    score: float


class CategoryData(BaseModel):
    id: int
    name: str
    display_name: str | None
    created_at: datetime | None
    updated_at: datetime | None
