from fastapi import Depends

from src.payment.repository import PaymentRepo
from src.payment.service import PaymentService


async def get_payment_service(payment_repo: PaymentRepo = Depends()) -> PaymentService:
    return PaymentService(payment_repo)
