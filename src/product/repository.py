import asyncio
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.sql import Select

from src.database import database
from src.product.schemas import (
    ProductCreate,
    ProductData,
    ProductDatas,
    ProductRatingData,
    ProductReviewCreate,
    ProductReviewData,
    ProductReviewUpdate,
    ProductUpdate,
)
from src.product.table import (
    category_tb,
    product_category_tb,
    product_rating_tb,
    product_review_tb,
    product_tb,
)
from src.user.schemas import UserData
from src.user.table import user_tb


class ProductRepo:
    @staticmethod
    def get_base_select_query(
        ids: list[int] | None = None,
        owner_id: UUID | None = None,
        categories: list[str] | None = None,
        styles: list[str] | None = None,
        patterns: list[str] | None = None,
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
        if ids:
            select_query = select_query.where(product_tb.c.id.in_(ids))

        if categories:
            select_query = select_query.where(
                or_(
                    *[
                        category_tb.c.name.ilike(f"%{category}%")
                        for category in categories
                    ]
                )
            )

        if styles:
            select_query = select_query.where(
                or_(*[product_tb.c.style.ilike(f"%{style}%") for style in styles])
            )

        if patterns:
            select_query = select_query.where(
                or_(
                    *[
                        product_tb.c.pattern.ilike(f"%{pattern}%")
                        for pattern in patterns
                    ]
                )
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
    def get_total_rows_query(
        ids: list[int] | None = None,
        owner_id: UUID | None = None,
        categories: list[str] | None = None,
        styles: list[str] | None = None,
        patterns: list[str] | None = None,
        search_keyword: str | None = None,
    ) -> Select:
        select_query = select(func.count()).select_from(product_tb)

        if ids:
            select_query = select_query.where(product_tb.c.id.in_(ids))

        if categories:
            select_query = (
                select_query.join(product_category_tb)
                .join(category_tb)
                .where(
                    or_(
                        *[
                            category_tb.c.name.ilike(f"%{category}%")
                            for category in categories
                        ]
                    )
                )
            )

        if styles:
            select_query = select_query.where(
                or_(*[product_tb.c.style.ilike(f"%{style}%") for style in styles])
            )

        if patterns:
            select_query = select_query.where(
                or_(
                    *[
                        product_tb.c.pattern.ilike(f"%{pattern}%")
                        for pattern in patterns
                    ]
                )
            )

        if owner_id:
            select_query = select_query.where(product_tb.c.owner_id == owner_id)
        else:
            select_query = select_query.where(product_tb.c.is_public)

        if search_keyword:
            ilike_pattern = f"%{search_keyword}%"
            select_query = select_query.where(
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
        ids: list[int] | None = None,
        owner_id: UUID | None = None,
        categories: list[str] | None = None,
        styles: list[str] | None = None,
        patterns: list[str] | None = None,
        search_keyword: str | None = None,
        offset: int | None = None,
        size: int | None = None,
    ) -> ProductDatas:
        select_query = self.get_base_select_query(
            ids=ids,
            owner_id=owner_id,
            categories=categories,
            styles=styles,
            patterns=patterns,
            search_keyword=search_keyword,
            offset=offset,
            size=size,
        )
        select_total_row_query = self.get_total_rows_query(
            ids=ids,
            owner_id=owner_id,
            categories=categories,
            styles=styles,
            patterns=patterns,
            search_keyword=search_keyword,
        )
        results, total_rows = await asyncio.gather(
            database.fetch_all(select_query), database.fetch_val(select_total_row_query)
        )
        return ProductDatas(
            products=[ProductData(**result._mapping) for result in results],
            total_rows=total_rows,
        )

    async def get_categories(self) -> list[str]:
        select_query = select(category_tb.c.name)
        results = await database.fetch_all(select_query)
        return [result._mapping["name"] for result in results]

    async def get_styles(self) -> list[str]:
        return [
            "Cơ bản",
            "Hàn Quốc",
            "Thể thao",
            "Đường phố",
            "Công sở",
            "Nhiệt đới",
            "Tối giản",
            "Unisex",
            "Retro",
            "Boho",
            "Rách gối",
            "Cổ điển",
            "Sexy",
        ]

    async def get_patterns(self) -> list[str]:
        return [
            "In",
            "Họa tiết",
            "Trơn",
            "Khác",
            "Phụ kiện kèm",
            "Sọc caro",
            "Rách gối",
            "Phối",
            "Rách gấu",
            "Form ôm",
            "Chấm bi",
            "Sọc",
        ]

    async def get_by_id_and_user_id(
        self, product_id: int, user_id: UUID
    ) -> ProductData | None:
        select_query = (
            select(
                product_tb,
                func.array_agg(category_tb.c.name).label("categories"),
                product_rating_tb.c.score.label("my_rating_score"),
            )
            .select_from(product_tb)
            .join(product_category_tb, isouter=True)
            .join(category_tb, isouter=True)
            .join(
                product_rating_tb,
                isouter=True,
                onclause=and_(
                    product_tb.c.id == product_rating_tb.c.product_id,
                    product_rating_tb.c.user_id == user_id,
                ),
            )
            .group_by(product_tb.c.id, product_rating_tb.c.score)
        )
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

    async def get_product_reviews(self, product_id: int) -> list[ProductReviewData]:
        select_query = (
            select(
                product_review_tb,
                user_tb.c.email,
                user_tb.c.first_name,
                user_tb.c.last_name,
                user_tb.c.avatar_url,
                product_rating_tb.c.score.label("rating_score"),
            )
            .select_from(product_review_tb)
            .join(user_tb)
            .join(
                product_rating_tb,
                isouter=True,
                onclause=and_(
                    product_review_tb.c.product_id == product_rating_tb.c.product_id,
                    product_review_tb.c.user_id == product_rating_tb.c.user_id,
                ),
            )
            .where(
                product_review_tb.c.product_id == product_id,
            )
            .order_by(product_review_tb.c.created_at.desc())
        )
        results = await database.fetch_all(select_query)
        return [
            ProductReviewData(
                **result._mapping,
                author=UserData(
                    id=result._mapping["user_id"],
                    email=result._mapping["email"],
                    first_name=result._mapping["first_name"],
                    last_name=result._mapping["last_name"],
                    avatar_url=result._mapping["avatar_url"],
                ),
            )
            for result in results
        ]

    async def get_product_review(
        self, user_id: UUID, product_id: int
    ) -> ProductReviewData | None:
        select_query = (
            select(
                product_review_tb,
                user_tb.c.email,
                user_tb.c.first_name,
                user_tb.c.last_name,
                user_tb.c.avatar_url,
            )
            .join(user_tb)
            .where(
                and_(
                    product_review_tb.c.product_id == product_id,
                    product_review_tb.c.user_id == user_id,
                )
            )
        )
        result = await database.fetch_one(select_query)
        return (
            ProductReviewData(
                **result._mapping,
                author=UserData(
                    id=result._mapping["user_id"],
                    email=result._mapping["email"],
                    first_name=result._mapping["first_name"],
                    last_name=result._mapping["last_name"],
                    avatar_url=result._mapping["avatar_url"],
                ),
            )
            if result
            else None
        )

    async def create_product(self, create_data: ProductCreate) -> ProductData:
        insert_query = (
            product_tb.insert().values(create_data.dict()).returning(product_tb)
        )
        result = await database.fetch_one(insert_query)
        return ProductData(**result._mapping)  # type: ignore

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

    async def create_product_review(
        self, create_data: ProductReviewCreate
    ) -> ProductReviewData:
        insert_query = (
            product_review_tb.insert()
            .values(create_data.dict())
            .returning(product_review_tb)
        )
        result = await database.fetch_one(insert_query)
        return ProductReviewData(**result._mapping)  # type: ignore

    async def update_product(
        self, product_id: int, update_data: ProductUpdate
    ) -> ProductData:
        update_query = (
            product_tb.update()
            .where(product_tb.c.id == product_id)
            .values(update_data.dict(exclude_unset=True))
            .returning(product_tb)
        )
        result = await database.fetch_one(update_query)
        return ProductData(**result._mapping)  # type: ignore

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

    async def update_product_review(
        self, user_id: UUID, product_id: int, update_data: ProductReviewUpdate
    ) -> ProductReviewData:
        update_query = (
            product_review_tb.update()
            .where(
                and_(
                    product_review_tb.c.user_id == user_id,
                    product_review_tb.c.product_id == product_id,
                )
            )
            .values(update_data.dict())
            .returning(product_review_tb)
        )
        result = await database.fetch_one(update_query)
        return ProductReviewData(**result._mapping)  # type: ignore

    async def delete_product_rating(self, user_id: UUID, product_id: int) -> None:
        delete_query = product_rating_tb.delete().where(
            and_(
                product_rating_tb.c.user_id == user_id,
                product_rating_tb.c.product_id == product_id,
            )
        )
        await database.execute(delete_query)

    async def delete_product_review(self, user_id: UUID, product_id: int) -> None:
        delete_query = product_review_tb.delete().where(
            and_(
                product_review_tb.c.user_id == user_id,
                product_review_tb.c.product_id == product_id,
            )
        )
        await database.execute(delete_query)
