from uuid import UUID

from sqlalchemy import delete, func, insert, select

from src.closet.schemas import ClosetCreate, ClosetData
from src.closet.table import closet_item_tb, closet_tb
from src.database import database
from src.product.schemas import ProductData
from src.product.table import category_tb, product_category_tb, product_tb


class ClosetRepo:
    async def create(self, create_data: ClosetCreate) -> ClosetData:
        async with database.transaction() as transaction:
            insert_query = (
                insert(closet_tb)
                .values(**create_data.dict(exclude_none=True, exclude={"product_ids"}))
                .returning(closet_tb)
            )
            result = await database.fetch_one(insert_query)
            new_closet = ClosetData(**result._mapping)  # type: ignore

            await transaction.commit()
            return new_closet

    async def create_closet_items(self, closet_id: UUID, product_ids: list[int]):
        insert_query = insert(closet_item_tb).values(
            [
                {"closet_id": closet_id, "product_id": product_id}
                for product_id in product_ids
            ]
        )
        await database.fetch_all(insert_query)

    async def delete_closet_items(self, closet_id: UUID, product_ids: list[int]):
        delete_query = (
            delete(closet_item_tb)
            .where(closet_item_tb.c.closet_id == closet_id)
            .where(closet_item_tb.c.product_id.in_(product_ids))
        )
        await database.fetch_all(delete_query)

    async def get_by_owner_id(self, owner_id: UUID) -> ClosetData | None:
        select_query = select(closet_tb).where(closet_tb.c.owner_id == owner_id)
        result = await database.fetch_one(select_query)
        return ClosetData(**result._mapping) if result else None

    async def get_closet_items(self, closet_id: UUID) -> list[ProductData]:
        select_query = (
            select(
                product_tb,
                func.array_agg(category_tb.c.name).label("categories"),
            )
            .select_from(closet_item_tb)
            .join(product_tb)
            .join(product_category_tb, isouter=True)
            .join(category_tb, isouter=True)
            .where(closet_item_tb.c.closet_id == closet_id)
            .group_by(product_tb.c.id)
        )
        results = await database.fetch_all(select_query)
        return [ProductData(**result._mapping) for result in results]

    async def delete_by_owner_id(self, owner_id: UUID) -> None:
        await database.fetch_one(
            closet_tb.delete().where(closet_item_tb.c.owner_id == owner_id)
        )
