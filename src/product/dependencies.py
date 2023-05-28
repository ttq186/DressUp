from fastapi import Depends

from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData
from src.product.exceptions import NotReviewedProductYet, ProductPermissionDenied
from src.product.repository import ProductRepo
from src.product.schemas import ProductData, ProductReviewData
from src.product.service import ProductService


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


async def valid_product_review(
    product: ProductData = Depends(valid_product_id),
    jwt_data: JWTData = Depends(valid_jwt_token),
    product_repo: ProductRepo = Depends(),
) -> ProductReviewData:
    product_review = await product_repo.get_product_review(
        user_id=jwt_data.user_id, product_id=product.id
    )
    if not product_review:
        raise NotReviewedProductYet()
    return product_review
