from uuid import UUID

from sqlalchemy import insert, select

from src.closet.schemas import ClosetCreate, ClosetData, ClosetUpdate
from src.closet.table import closet_item_tb, closet_tb
from src.database import database
from src.product.table import product_tb


class ClosetRepo:
    async def create(self, create_data: ClosetCreate) -> ClosetData:
        async with database.transaction() as transaction:
            insert_query = (
                insert(closet_tb)
                .values(**create_data.dict(exclude_none=True))
                .returning(closet_tb)
            )
            result = await database.fetch_one(insert_query)
            new_closet = ClosetData(**result._mapping)  # type: ignore

            if create_data.product_ids:
                insert_query = (
                    insert(closet_item_tb)
                    .values(
                        {"closet_id": new_closet.id, "product_id": product_id}
                        for product_id in create_data.product_ids
                    )
                    .returning(closet_item_tb)
                )
                results = await database.fetch_all(insert_query)
                new_closet.product_ids = [
                    result._mapping["product_id"] for result in results
                ]
            await transaction.commit()
            return new_closet

    async def get_by_owner_id(self, owner_id: UUID) -> ClosetData:
        select_query = (
            select(closet_tb, product_tb)
            .select_from(closet_tb)
            .join(closet_item_tb)
            .join(product_tb)
        )
        return select_query

    async def update_by_owner_id(
        self, owner_id: UUID, update_data: ClosetUpdate
    ) -> ClosetData:
        pass

    async def delete_by_owner_id(self, owner_id: UUID) -> None:
        pass
