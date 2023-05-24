from uuid import UUID

from fastapi import Depends

from src.product.repository import ProductRepo
from src.product.service import ProductService


async def get_product_service(product_repo: ProductRepo = Depends()) -> ProductService:
    return ProductService(product_repo)


async def valid_product_id(product_id: UUID):
    pass
