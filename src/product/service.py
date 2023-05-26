from uuid import UUID

from src.product.repository import ProductRepo
from src.product.schemas import CategoryData, ProductData


class ProductService:
    def __init__(self, product_repo: ProductRepo):
        self.product_repo = product_repo

    async def get_products(
        self,
        owner_id: UUID | None = None,
        search_keyword: str | None = None,
        size: int = 20,
        offset: int = 0,
    ) -> list[ProductData]:
        return await self.product_repo.get_multi(
            owner_id=owner_id, search_keyword=search_keyword, size=size, offset=offset
        )

    async def get_my_products(
        self,
        owner_id: UUID,
        search_keyword: str | None = None,
        size: int = 20,
        offset: int = 0,
    ) -> list[ProductData]:
        return await self.product_repo.get_multi(
            owner_id=owner_id, search_keyword=search_keyword, size=size, offset=offset
        )

    async def get_categories(self) -> list[CategoryData]:
        return await self.product_repo.get_categories()

    async def rate_product(
        self, user_id: UUID, product: ProductData, score: float
    ) -> ProductData:
        product_rating = await self.product_repo.get_product_rating(
            user_id=user_id, product_id=product.id
        )
        if not product_rating:
            product_rating = await self.product_repo.create_product_rating(
                user_id=user_id, product_id=product.id, score=score
            )
        else:
            product_rating = await self.product_repo.update_product_rating(
                user_id=user_id, product_id=product.id, score=score
            )
        return ProductData(
            **product.dict(exclude={"my_rating_score"}),
            my_rating_score=product_rating.score
        )

    async def unrate_product(self, user_id: UUID, product_id: int):
        await self.product_repo.delete_product_rating(
            user_id=user_id, product_id=product_id
        )
