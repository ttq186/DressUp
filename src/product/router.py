from fastapi import APIRouter, Body, Depends, Query, status

from src.auth.dependencies import valid_jwt_token, valid_user
from src.auth.schemas import JWTData
from src.product.dependencies import (
    get_product_service,
    valid_product_id,
    valid_product_review,
)
from src.product.exceptions import AlreadyReviewedProduct, ProductNotRatedYet
from src.product.schemas import (
    CategoryData,
    ProductData,
    ProductDatas,
    ProductReviewCreate,
    ProductReviewData,
    ProductReviewUpdate,
)
from src.product.service import ProductService
from src.user.schemas import UserData

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
async def get_products(
    search_keyword: str | None = None,
    size: int = Query(default=20, ge=1),
    offset: int = Query(default=0, ge=0),
    service: ProductService = Depends(get_product_service),
) -> ProductDatas:
    return await service.get_products(
        search_keyword=search_keyword, size=size, offset=offset
    )


@router.get("/me")
async def get_my_products(
    search_keyword: str | None = None,
    size: int = Query(default=20, ge=1),
    offset: int = Query(default=0, ge=0),
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ProductService = Depends(get_product_service),
) -> ProductDatas:
    return await service.get_products(
        owner_id=jwt_data.user_id,
        search_keyword=search_keyword,
        size=size,
        offset=offset,
    )


@router.get("/categories")
async def get_categories(
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ProductService = Depends(get_product_service),
) -> list[CategoryData]:
    return await service.get_categories()


@router.get("/{product_id}")
async def get_product(product: ProductData = Depends(valid_product_id)) -> ProductData:
    return product


@router.put("/{product_id}/rating")
async def rate_product(
    score: float = Body(embed=True, ge=0.5, lt=5),
    product: ProductData = Depends(valid_product_id),
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ProductService = Depends(get_product_service),
) -> ProductData:
    return await service.rate_product(
        product=product, user_id=jwt_data.user_id, score=score
    )


@router.delete("/{product_id}/rating", status_code=status.HTTP_204_NO_CONTENT)
async def unrate_product(
    product: ProductData = Depends(valid_product_id),
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ProductService = Depends(get_product_service),
):
    if not product.my_rating_score:
        raise ProductNotRatedYet()
    await service.unrate_product(product_id=product.id, user_id=jwt_data.user_id)


@router.post("/{product_id}/reviews")
async def review_product(
    product_review_create: ProductReviewCreate,
    product: ProductData = Depends(valid_product_id),
    user: UserData = Depends(valid_user),
    service: ProductService = Depends(get_product_service),
) -> ProductReviewData:
    product_review = await service.get_product_review(
        user_id=user.id, product_id=product.id
    )
    if product_review:
        raise AlreadyReviewedProduct()
    return await service.review_product(
        author=user, product=product, create_data=product_review_create
    )


@router.get("/{product_id}/reviews", response_model_exclude_unset=True)
async def get_product_reviews(
    product: ProductData = Depends(valid_product_id),
    service: ProductService = Depends(get_product_service),
) -> list[ProductReviewData]:
    return await service.get_product_reviews(product_id=product.id)


@router.get(
    "/{product_id}/reviews/me", response_model_exclude={"author"}
)
async def get_my_product_review(
    product_review: ProductReviewData = Depends(valid_product_review),
) -> ProductReviewData:
    return product_review


@router.put("/{product_id}/reviews/me", response_model_exclude={"author"})
async def update_my_product_review(
    product_review_update: ProductReviewUpdate,
    product_review: ProductReviewData = Depends(valid_product_review),
    service: ProductService = Depends(get_product_service),
) -> ProductReviewData:
    return await service.update_product_review(
        product_review=product_review, update_data=product_review_update
    )


@router.delete("/{product_id}/reviews/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_product_review(
    product_review: ProductReviewData = Depends(valid_product_review),
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ProductService = Depends(get_product_service),
):
    return await service.delete_product_review(
        product_id=product_review.product_id, user_id=jwt_data.user_id
    )
