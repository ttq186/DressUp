from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.sql import Select

from src.database import database
from src.product.schemas import ProductData, ProductRatingData
from src.product.table import (
    category_tb,
    product_category_tb,
    product_rating_tb,
    product_tb,
)


class ProductRepo:
    @staticmethod
    async def get_base_select_query(
        owner_id: UUID | None = None,
        search_keyword: str | None = None,
        offset: int | None = None,
        size: int | None = None,
    ) -> Select:
        select_query = (
            select(
                product_tb,
                func.array_agg(category_tb.c.name).label("categories"),
            )
            .select_from(product_tb)
            .join(product_category_tb)
            .join(category_tb)
            .group_by(product_tb.c.id)
        )

        if owner_id:
            select_query = select_query.filter(product_tb.c.owner_id == owner_id)
        else:
            select_query = select_query.filter(product_tb.c.is_public)

        if search_keyword:
            ilike_pattern = f"%{search_keyword}%"
            select_query = select_query.filter(
                or_(
                    product_tb.c.name.ilike(ilike_pattern),
                    product_tb.c.description.ilike(ilike_pattern),
                    product_tb.c.brand.ilike(ilike_pattern),
                    product_tb.c.pattern.ilike(ilike_pattern),
                    product_tb.c.style.ilike(ilike_pattern),
                )
            )

        if offset:
            select_query = select_query.offset(offset)

        if size:
            select_query = select_query.limit(size)

        return select_query

    async def get_multi(
        self,
        owner_id: UUID | None = None,
        search_keyword: str | None = None,
        offset: int | None = None,
        size: int | None = None,
    ) -> list[ProductData]:
        select_query = await self.get_base_select_query(
            owner_id=owner_id, search_keyword=search_keyword, offset=offset, size=size
        )
        results = await database.fetch_all(select_query)
        return [ProductData(**result._mapping) for result in results]

    async def create_product_rating(
        self, user_id: UUID, product_id: int, score: int
    ) -> ProductRatingData:
        insert_query = product_rating_tb.insert(
            user_id=user_id, product_id=product_id, score=score
        )
        result = await database.fetch_one(insert_query)
        return ProductRatingData(**result._mapping)  # type: ignore
