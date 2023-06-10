from uuid import UUID

from src.payment.repository import PaymentRepo
from src.payment.schemas import PaymentCreate, PaymentData


class PaymentService:
    def __init__(self, payment_repo: PaymentRepo):
        self.payment_repo = payment_repo

    async def create_history(
        self, user_id: UUID, create_data: PaymentCreate
    ) -> PaymentData:
        create_data.user_id = user_id
        return await self.payment_repo.create_history(create_data=create_data)
