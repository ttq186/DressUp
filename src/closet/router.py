from fastapi import APIRouter, Depends, status

from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData
from src.closet.dependencies import (
    get_closet_service,
    valid_closet,
    valid_closet_update,
)
from src.closet.schemas import ClosetData, ClosetUpdate
from src.closet.service import ClosetService

router = APIRouter(prefix="/closets", tags=["Closets"])


@router.get("/me")
async def get_or_create_if_not_exist_my_closet(
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ClosetService = Depends(get_closet_service),
) -> ClosetData:
    return await service.get_closet(owner_id=jwt_data.user_id)


@router.put("/me")
async def update_my_closet(
    closet_update: ClosetUpdate = Depends(valid_closet_update),
    closet: ClosetData = Depends(valid_closet),
    service: ClosetService = Depends(get_closet_service),
) -> ClosetData:
    return await service.update_closet(closet=closet, update_data=closet_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_closet(
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: ClosetService = Depends(get_closet_service),
):
    await service.delete_closet(owner_id=jwt_data.user_id)
