from fastapi import APIRouter, Depends

from src.user.dependencies import get_user_service, valid_user
from src.user.schemas import UserData, UserUpdate
from src.user.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model_exclude={"password"})
async def get_my_profile(user: UserData = Depends(valid_user)) -> UserData:
    return user


@router.put("/me", response_model_exclude={"password"})
async def update_my_profile(
    user_update: UserUpdate,
    user: UserData = Depends(valid_user),
    service: UserService = Depends(get_user_service),
) -> UserData:
    return await service.update_user(user=user, update_data=user_update)
