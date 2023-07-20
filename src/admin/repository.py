from sqlalchemy import case, func, or_, select

from src.admin.schemas import AdminUserData
from src.auth.constants import UserRole
from src.database import database
from src.payment.constants import PaymentStatus
from src.payment.table import payment_history_tb
from src.user.constants import SubscriptionType
from src.user.table import user_tb


class AdminRepo:
    async def get_users(
        self,
        subscription_type: SubscriptionType | None = None,
        is_active: bool | None = None,
        is_activated: bool | None = None,
        search_keyword: str | None = None,
    ) -> list[AdminUserData]:
        sub_query = (
            select(
                payment_history_tb.c.user_id,
                func.sum(payment_history_tb.c.price).label("total_paid_amount"),
            )
            .where(payment_history_tb.c.status == PaymentStatus.SUCCESS)
            .group_by(payment_history_tb.c.user_id)
            .subquery()
        )

        total_paid_amount_col = func.coalesce(sub_query.c.total_paid_amount)
        subscription_type_col = case(  # type: ignore
            (total_paid_amount_col == 14000, SubscriptionType.PREMIUM1),
            (total_paid_amount_col == 17000, SubscriptionType.PREMIUM1),
            (total_paid_amount_col == 150000, SubscriptionType.PREMIUM2),
            (total_paid_amount_col == 180000, SubscriptionType.PREMIUM2),
            else_=SubscriptionType.FREE,
        )

        select_query = (
            select(
                user_tb,
                func.coalesce(total_paid_amount_col, 0).label("total_paid_amount"),
                subscription_type_col.label("subscription_type"),
            )
            .select_from(user_tb)
            .join(sub_query, onclause=user_tb.c.id == sub_query.c.user_id, isouter=True)
        )
        if is_active is not None:
            select_query = select_query.where(user_tb.c.is_active == is_active)

        if is_activated is not None:
            select_query = select_query.where(user_tb.c.is_activated == is_activated)

        if subscription_type:
            select_query = select_query.where(
                subscription_type_col == subscription_type
            )

        if search_keyword:
            ilike_pattern = f"%{search_keyword}%"
            select_query = select_query.filter(
                or_(
                    user_tb.c.first_name.ilike(ilike_pattern),
                    user_tb.c.last_name.ilike(ilike_pattern),
                    user_tb.c.email.ilike(ilike_pattern),
                )
            )
        select_query = select_query.where(user_tb.c.role == UserRole.USER)

        results = await database.fetch_all(select_query)
        return [AdminUserData(**result._mapping) for result in results]
