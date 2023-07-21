from fastapi import APIRouter, Depends

from src.admin.dependencies import get_admin_service, valid_admin_jwt_token
from src.admin.schemas import AdminUserData
from src.admin.service import AdminService
from src.auth.schemas import JWTData
from src.user.constants import SubscriptionType

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model_exclude={"password"})
async def get_users(
    # jwt_data: JWTData = Depends(valid_admin_jwt_token),
    search_keyword: str | None = None,
    subscription_type: SubscriptionType | None = None,
    is_active: bool | None = None,
    is_activated: bool | None = None,
    service: AdminService = Depends(get_admin_service),
) -> list[AdminUserData]:
    return await service.get_users(
        search_keyword=search_keyword,
        subscription_type=subscription_type,
        is_active=is_active,
        is_activated=is_activated,
    )
