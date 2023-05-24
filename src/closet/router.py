from fastapi import APIRouter, Depends, status

from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData
from src.closet.dependencies import get_closet_service
from src.closet.schemas import ClosetData, ClosetUpdate
from src.closet.service import ClosetService

router = APIRouter(prefix="/closet", tags=["Closets"])


@router.get("/me")
async def get_my_closet(
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ClosetService = Depends(get_closet_service),
) -> ClosetData:
    return await service.get_closet(owner_id=jwt_data.user_id)


@router.put("/me")
async def update_my_closet(
    closet_update: ClosetUpdate,
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ClosetService = Depends(get_closet_service),
) -> ClosetData:
    return await service.update_closet(owner_id=jwt_data.user_id)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_closet(
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ClosetService = Depends(get_closet_service),
):
    await service.delete_closet(owner_id=jwt_data.user_id)
