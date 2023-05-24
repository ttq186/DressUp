from fastapi import Depends

from src.closet.repository import ClosetRepo
from src.closet.service import ClosetService
from src.product.repository import ProductRepo


async def get_closet_service(
    closet_repo: ClosetRepo = Depends(), product_repo: ProductRepo = Depends()
) -> ClosetService:
    return ClosetService(closet_repo)
