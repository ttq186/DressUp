from fastapi import Depends

from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData
from src.closet.exceptions import (
    AtLeastOneProductAlreadyInCloset,
    AtLeastOneProductNotInCloset,
    ProductCantBeAddedAndRemoved,
)
from src.closet.repository import ClosetRepo
from src.closet.schemas import ClosetData, ClosetUpdate
from src.closet.service import ClosetService
from src.product.repository import ProductRepo


async def get_closet_service(
    closet_repo: ClosetRepo = Depends(), product_repo: ProductRepo = Depends()
) -> ClosetService:
    return ClosetService(closet_repo, product_repo)


async def valid_closet(
    jwt_data: JWTData = Depends(valid_jwt_token),
    closet_service: ClosetService = Depends(get_closet_service),
) -> ClosetData:
    return await closet_service.get_closet(owner_id=jwt_data.user_id)


async def valid_closet_update(
    closet_update: ClosetUpdate,
    closet: ClosetData = Depends(valid_closet),
) -> ClosetUpdate:
    product_ids = [
        product.id for product in [*closet.owned_products, *closet.public_products]
    ]
    added_product_ids = closet_update.added_product_ids
    removed_product_ids = closet_update.removed_product_ids

    if set(added_product_ids).intersection(removed_product_ids):
        raise ProductCantBeAddedAndRemoved()

    if set(added_product_ids).intersection(product_ids):
        raise AtLeastOneProductAlreadyInCloset()

    if not set(removed_product_ids).issubset(product_ids):
        raise AtLeastOneProductNotInCloset()
    return closet_update
