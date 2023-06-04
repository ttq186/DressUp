from uuid import UUID

from src.product.repository import ProductRepo
from src.product.schemas import (
    CategoryData,
    ProductData,
    ProductDatas,
    ProductReviewCreate,
    ProductReviewData,
    ProductReviewUpdate,
)
from src.user.schemas import UserData


class ProductService:
    def __init__(self, product_repo: ProductRepo):
        self.product_repo = product_repo

    async def get_products(
        self,
        owner_id: UUID | None = None,
        categories: list[str] | None = None,
        search_keyword: str | None = None,
        size: int = 20,
        offset: int = 0,
    ) -> ProductDatas:
        return await self.product_repo.get_multi(
            owner_id=owner_id,
            categories=categories,
            search_keyword=search_keyword,
            size=size,
            offset=offset,
        )

    async def get_my_products(
        self,
        owner_id: UUID,
        categories: list[str] | None = None,
        search_keyword: str | None = None,
        size: int = 20,
        offset: int = 0,
    ) -> ProductDatas:
        return await self.product_repo.get_multi(
            owner_id=owner_id,
            categories=categories,
            search_keyword=search_keyword,
            size=size,
            offset=offset,
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

    async def get_product_reviews(self, product_id: int) -> list[ProductReviewData]:
        return await self.product_repo.get_product_reviews(product_id)

    async def get_product_review(
        self, user_id: UUID, product_id: int
    ) -> ProductReviewData | None:
        return await self.product_repo.get_product_review(
            user_id=user_id, product_id=product_id
        )

    async def review_product(
        self, author: UserData, product: ProductData, create_data: ProductReviewCreate
    ) -> ProductReviewData:
        create_data.product_id = product.id
        create_data.user_id = author.id
        product_review = await self.product_repo.create_product_review(create_data)
        product_review.author = author
        product_review.rating_score = product.my_rating_score
        return product_review

    async def update_product_review(
        self, product_review: ProductReviewData, update_data: ProductReviewUpdate
    ) -> ProductReviewData:
        return await self.product_repo.update_product_review(
            user_id=product_review.author.id,  # type: ignore
            product_id=product_review.product_id,
            update_data=update_data,
        )

    async def delete_product_review(self, user_id: UUID, product_id: int) -> None:
        await self.product_repo.delete_product_review(
            user_id=user_id, product_id=product_id
        )
