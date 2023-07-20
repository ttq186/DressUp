from src.admin.repository import AdminRepo
from src.admin.schemas import AdminUserData
from src.user.constants import SubscriptionType


class AdminService:
    def __init__(self, admin_repo: AdminRepo):
        self.admin_repo = admin_repo

    async def get_users(
        self,
        subscription_type: SubscriptionType | None = None,
        is_active: bool | None = None,
        is_activated: bool | None = None,
        search_keyword: str | None = None,
    ) -> list[AdminUserData]:
        return await self.admin_repo.get_users(
            search_keyword=search_keyword,
            subscription_type=subscription_type,
            is_active=is_active,
            is_activated=is_activated,
        )
