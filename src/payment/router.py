from fastapi import APIRouter, Depends

from src.auth.dependencies import valid_jwt_token
from src.auth.schemas import JWTData
from src.payment.dependencies import get_payment_service
from src.payment.schemas import PaymentCreate, PaymentData
from src.payment.service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/request")
async def create_payment_request(
    payment_create: PaymentCreate,
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentData:
    return await service.create_history(
        user_id=jwt_data.user_id, create_data=payment_create
    )
