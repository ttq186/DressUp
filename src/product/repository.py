from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.sql import Select

from src.database import database
from src.product.schemas import ProductData
from src.product.table import category_tb, product_category_tb, product_tb


class ProductRepo:
    @staticmethod
    async def get_base_select_query(
        search_keyword: str | None = None,
        offset: int | None = None,
        size: int | None = None,
    ) -> Select:
        select_query = (
            select(product_tb, func.array_agg(category_tb.c.name).label("categories"))
            .select_from(product_tb)
            .join(product_category_tb)
            .join(category_tb)
            .group_by(product_tb.c.id)
        )

        if search_keyword:
            ilike_pattern = f"%{search_keyword}%"
            select_query = select_query.filter(
                or_(
                    product_tb.c.name.ilike(ilike_pattern),
                    product_tb.c.description.ilike(ilike_pattern),
                    product_tb.c.brand.ilike(ilike_pattern),
                )
            )

        if offset:
            select_query = select_query.offset(offset)

        if size:
            select_query = select_query.limit(size)

        return select_query

    async def get_multi(
        self,
        search_keyword: str | None = None,
        offset: int | None = None,
        size: int | None = None,
    ) -> list[ProductData]:
        select_query = await self.get_base_select_query(
            search_keyword=search_keyword, offset=offset, size=size
        )
        results = await database.fetch_all(select_query)
        return [ProductData(**result._mapping) for result in results]

    async def get_multi_by_user_id(self) -> list[ProductData]:
        select_query = select(product_tb).where(product_tb.c.id == id)
        result = await database.fetch_one(select_query)
        return ProductData(**result._mapping) if result else None

    async def get_public_and_owned_products(self, owner_id: UUID) -> list[ProductData]:
        select_query = select(product_tb).where(product_tb.c.id == id)
        result = await database.fetch_one(select_query)
        return ProductData(**result._mapping) if result else None
