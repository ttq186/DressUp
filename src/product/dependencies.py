from fastapi import Depends

from src.product.repository import ProductRepo
from src.product.service import ProductService
from src.product.schemas import ProductData
from src.auth.schemas import JWTData
from src.auth.dependencies import valid_jwt_token
from src.product.exceptions import ProductPermissionDenied


async def get_product_service(product_repo: ProductRepo = Depends()) -> ProductService:
    return ProductService(product_repo)


async def valid_product_id(
    product_id: int,
    jwt_data: JWTData = Depends(valid_jwt_token),
    product_repo: ProductRepo = Depends(),
) -> ProductData:
    product = await product_repo.get_by_id_and_user_id(
        product_id=product_id, user_id=jwt_data.user_id
    )
    if not product:
        raise ProductPermissionDenied()

    return product
