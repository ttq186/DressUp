from uuid import UUID

from src.closet.repository import ClosetRepo
from src.closet.schemas import ClosetCreate, ClosetData, ClosetUpdate
from src.product.repository import ProductRepo
from src.product.schemas import ProductData


class ClosetService:
    def __init__(self, closet_repo: ClosetRepo, product_repo: ProductRepo):
        self.closet_repo = closet_repo
        self.product_repo = product_repo

    async def create_closet(self, create_data: ClosetCreate) -> ClosetData:
        pass

    async def get_or_create_closet_if_not_exist(self, owner_id: UUID) -> ClosetData:
        closet = await self.closet_repo.get_by_owner_id(owner_id=owner_id)
        if not closet:
            closet = await self.closet_repo.create(
                create_data=ClosetCreate(owner_id=owner_id)
            )
        # if closet.product_ids:
        #     self.product_repo.get_multi_by_user_id
        return closet

    async def get_closet_items(self, closet_id: UUID) -> list[ProductData]:
        return await self.closet_repo.get_closet_items(closet_id=closet_id)

    async def get_closet(self, owner_id: UUID) -> ClosetData:
        closet = await self.get_or_create_closet_if_not_exist(owner_id=owner_id)
        closet_items = await self.get_closet_items(closet_id=closet.id)
        closet.owned_products = [
            closet_item
            for closet_item in closet_items
            if closet_item.owner_id == owner_id
        ]
        closet.public_products = [
            closet_item
            for closet_item in closet_items
            if closet_item.owner_id != owner_id
        ]
        return closet

    async def update_closet(
        self, closet: ClosetData, update_data: ClosetUpdate
    ) -> ClosetData:
        if update_data.removed_product_ids:
            await self.closet_repo.delete_closet_items(
                closet_id=closet.id, product_ids=update_data.removed_product_ids
            )
        if update_data.added_product_ids:
            await self.closet_repo.create_closet_items(
                closet_id=closet.id, product_ids=update_data.added_product_ids
            )
        closet_items = await self.get_closet_items(closet_id=closet.id)
        closet.owned_products = [
            closet_item
            for closet_item in closet_items
            if closet_item.owner_id == closet.owner_id
        ]
        closet.public_products = [
            closet_item
            for closet_item in closet_items
            if closet_item.owner_id != closet.owner_id
        ]
        return closet

    async def delete_closet(self, owner_id: UUID) -> None:
        await self.closet_repo.delete_by_owner_id(owner_id=owner_id)
