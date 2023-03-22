from fastapi import APIRouter, Depends

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.user import service
from src.user.schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def get_my_profile(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    return await service.get_user_by_id(jwt_data.user_id)


@router.put("/me", response_model=UserOut)
async def update_my_profile(
    user_in: UserIn,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    await service.update_user(email=jwt_data.email, user_in=user_in)
    return await service.get_user_by_id(jwt_data.user_id)
