from fastapi import Depends

from src.admin.exceptions import AdminPermissionRequired
from src.admin.repository import AdminRepo
from src.admin.service import AdminService
from src.auth.constants import UserRole
from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData


async def get_admin_service(admin_repo: AdminRepo = Depends()) -> AdminService:
    return AdminService(admin_repo=admin_repo)


async def valid_admin_jwt_token(
    jwt_data: JWTData = Depends(valid_jwt_token),
) -> JWTData:
    if jwt_data.role != UserRole.ADMIN:
        raise AdminPermissionRequired()

    return jwt_data
