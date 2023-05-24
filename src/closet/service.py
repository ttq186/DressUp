from uuid import UUID

from src.closet.repository import ClosetRepo
from src.closet.schemas import ClosetCreate, ClosetData, ClosetUpdate
from src.product.repository import ProductRepo


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
        if closet.product_ids:
            self.product_repo.get_multi_by_user_id

        return closet

    async def get_closet_items(self, closet_id: UUID) -> list:
        pass

    async def get_closet(self, owner_id: UUID) -> ClosetData:
        closet = await self.get_or_create_closet_if_not_exist(owner_id=owner_id)
        closet_items = await self.get_closet_items(closet_id=closet.id)

    async def update_closet(self, update_data: ClosetUpdate) -> ClosetData:
        return await self.closet_repo.update_by_owner_id(
            owner_id=closet.owner_id, update_data=update_data
        )

    async def delete_closet(self, owner_id: UUID) -> None:
        await self.closet_repo.delete_by_owner_id(owner_id=owner_id)
