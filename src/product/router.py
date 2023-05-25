from fastapi import APIRouter, Body, Depends, Query

from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData
from src.product.dependencies import get_product_service
from src.product.schemas import ProductData
from src.product.service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
async def get_products(
    search_keyword: str | None = None,
    size: int = Query(default=20, ge=1),
    offset: int = Query(default=0, ge=0),
    service: ProductService = Depends(get_product_service),
) -> list[ProductData]:
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
) -> list[ProductData]:
    return await service.get_products(
        owner_id=jwt_data.user_id,
        search_keyword=search_keyword,
        size=size,
        offset=offset,
    )


@router.post("/{product_id}/rating")
async def rate_product(
    score: int = Body(embed=True, ge=1, lt=5),
    product: ProductData = Depends(),
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ProductService = Depends(get_product_service),
) -> ProductData:
    return await service.rate_product(
        product=product, user_id=jwt_data.user_id, score=score
    )
