from src.product.repository import ProductRepo
from src.product.schemas import ProductData


class ProductService:
    def __init__(self, product_repo: ProductRepo):
        self.product_repo = product_repo

    async def get_public_products(
        self, search_keyword: str | None = None, size: int = 20, offset: int = 0
    ) -> list[ProductData]:
        return await self.product_repo.get_multi(
            search_keyword=search_keyword, size=size, offset=offset
        )

    async def get_my_products(self) -> list[ProductData]:
        pass

    async def rate_product(self):
        self.product_repo
        return
