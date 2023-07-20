from sqlalchemy import insert

from src.database import database
from src.payment.constants import PaymentStatus
from src.payment.schemas import PaymentCreate, PaymentData
from src.payment.table import payment_history_tb


class PaymentRepo:
    async def create_history(self, create_data: PaymentCreate) -> PaymentData:
        insert_query = (
            insert(payment_history_tb)
            .values(**create_data.dict(), status=PaymentStatus.CHECKING)
            .returning(payment_history_tb)
        )
        result = await database.fetch_one(insert_query)
        return PaymentData(**result._mapping)  # type: ignore
