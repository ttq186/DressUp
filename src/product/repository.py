import asyncio
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.sql import Select

from src.database import database
from src.product.schemas import (
    CategoryData,
    ProductData,
    ProductDatas,
    ProductRatingData,
)
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
                product_rating_tb.c.score.label("my_rating_score"),
            )
            .select_from(product_tb)
            .join(product_category_tb)
            .join(category_tb)
            .join(product_rating_tb, isouter=True)
            .group_by(product_tb.c.id, product_rating_tb.c.score)
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

    @staticmethod
    async def get_total_rows(
        owner_id: UUID | None = None,
        search_keyword: str | None = None,
    ) -> Select:
        select_query = select(func.count())
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
        return select_query

    async def get_multi(
        self,
        owner_id: UUID | None = None,
        search_keyword: str | None = None,
        offset: int | None = None,
        size: int | None = None,
    ) -> ProductDatas:
        select_query = await self.get_base_select_query(
            owner_id=owner_id, search_keyword=search_keyword, offset=offset, size=size
        )
        select_total_row_query = await self.get_total_rows(
            owner_id=owner_id, search_keyword=search_keyword
        )
        results, total_rows = await asyncio.gather(
            database.fetch_all(select_query), database.fetch_val(select_total_row_query)
        )
        return ProductDatas(
            products=[ProductData(**result._mapping) for result in results],
            total_rows=total_rows,
        )

    async def get_categories(self) -> list[CategoryData]:
        select_query = category_tb.select()
        results = await database.fetch_all(select_query)
        return [CategoryData(**result._mapping) for result in results]

    async def get_by_id_and_user_id(
        self, product_id: int, user_id: UUID
    ) -> ProductData | None:
        select_query = await self.get_base_select_query()
        select_query = select_query.where(product_tb.c.id == product_id).where(
            or_(product_tb.c.owner_id == user_id, product_tb.c.is_public)
        )
        result = await database.fetch_one(select_query)
        return ProductData(**result._mapping) if result else None

    async def get_product_rating(
        self, user_id: UUID, product_id: int
    ) -> ProductRatingData | None:
        select_query = product_rating_tb.select().where(
            and_(
                product_rating_tb.c.user_id == user_id,
                product_rating_tb.c.product_id == product_id,
            )
        )
        result = await database.fetch_one(select_query)
        return ProductRatingData(**result._mapping) if result else None

    async def create_product_rating(
        self, user_id: UUID, product_id: int, score: float
    ) -> ProductRatingData:
        insert_query = (
            product_rating_tb.insert()
            .values(user_id=user_id, product_id=product_id, score=score)
            .returning(product_rating_tb)
        )
        result = await database.fetch_one(insert_query)
        return ProductRatingData(**result._mapping)  # type: ignore

    async def update_product_rating(
        self, user_id: UUID, product_id: int, score: float
    ) -> ProductRatingData:
        update_query = (
            product_rating_tb.update()
            .where(
                and_(
                    product_rating_tb.c.user_id == user_id,
                    product_rating_tb.c.product_id == product_id,
                )
            )
            .values(score=score)
            .returning(product_rating_tb)
        )
        result = await database.fetch_one(update_query)
        return ProductRatingData(**result._mapping)  # type: ignore

    async def delete_product_rating(self, user_id: UUID, product_id: int) -> None:
        delete_query = product_rating_tb.delete().where(
            and_(
                product_rating_tb.c.user_id == user_id,
                product_rating_tb.c.product_id == product_id,
            )
        )
        await database.execute(delete_query)
