from uuid import UUID

import httpx

from src.closet.schemas import ClosetData
from src.config import settings
from src.product.repository import ProductRepo
from src.product.schemas import (
    ProductCreate,
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

    async def create_product(self, create_data: ProductCreate) -> ProductData:
        return await self.product_repo.create_product(create_data)

    async def get_products(
        self,
        ids: list[int] | None = None,
        owner_id: UUID | None = None,
        categories: list[str] | None = None,
        styles: list[str] | None = None,
        patterns: list[str] | None = None,
        search_keyword: str | None = None,
        size: int = 20,
        offset: int = 0,
    ) -> ProductDatas:
        return await self.product_repo.get_multi(
            ids=ids,
            owner_id=owner_id,
            categories=categories,
            styles=styles,
            patterns=patterns,
            search_keyword=search_keyword,
            size=size,
            offset=offset,
        )

    async def get_my_products(
        self,
        owner_id: UUID,
        categories: list[str] | None = None,
        styles: list[str] | None = None,
        patterns: list[str] | None = None,
        search_keyword: str | None = None,
        size: int = 20,
        offset: int = 0,
    ) -> ProductDatas:
        return await self.product_repo.get_multi(
            owner_id=owner_id,
            categories=categories,
            styles=styles,
            patterns=patterns,
            search_keyword=search_keyword,
            size=size,
            offset=offset,
        )

    async def get_recommendations(
        self,
        closet: ClosetData,
        include_public_products: bool,
        size: int,
    ) -> ProductDatas:
        if include_public_products:
            referenced_products = [*closet.owned_products, *closet.public_products]
        else:
            referenced_products = closet.owned_products

        if not referenced_products:
            return ProductDatas(products=[], total_rows=0)

        referenced_product_img_urls = []
        for product in referenced_products:
            referenced_product_img_urls.extend(product.image_urls)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{settings.AI_MODEL_URL}/recommendation",
                json={
                    "image_urls": referenced_product_img_urls,
                    "num_of_recommended_products": size,
                },
                timeout=None,
            )
            recommended_product_ids = response.json()
        return await self.get_products(ids=recommended_product_ids, size=size)

    async def get_categories(self) -> list[str]:
        return await self.product_repo.get_categories()

    async def get_styles(self) -> list[str]:
        return await self.product_repo.get_styles()

    async def get_patterns(self) -> list[str]:
        return await self.product_repo.get_patterns()

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
            my_rating_score=product_rating.score,
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
