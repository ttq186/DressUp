from fastapi import APIRouter, BackgroundTasks, Body, Depends, Response, status

from src.auth import jwt, utils
from src.auth.constants import SuccessMessage
from src.auth.dependencies import (
    get_auth_service,
    valid_jwt_token,
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
    valid_user_email,
)
from src.auth.exceptions import AccountAlreadyActivated
from src.auth.schemas import (
    AuthData,
    JWTData,
    RefreshTokenData,
    TokenData,
    UserResetPassword,
)
from src.auth.service import AuthService
from src.aws.schemas import PresignedUrlData
from src.schemas import Message
from src.user.dependencies import get_user_service
from src.user.schemas import UserCreate, UserData
from src.user.service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def register_user(
    background_tasks: BackgroundTasks,
    user_create: UserCreate = Depends(valid_user_create),
    service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> Message:
    user = await user_service.create_user(user_create)
    await service.create_refresh_token(user_id=user.id)
    background_tasks.add_task(service.create_and_send_activate_email, user=user)
    return Message(detail=SuccessMessage.SUCCESS_ACCOUNT_CREATED)


@router.post("/users/activate/request")
async def request_activate_account(
    background_tasks: BackgroundTasks,
    user: UserData = Depends(valid_user_email),
    service: AuthService = Depends(get_auth_service),
) -> Message:
    if user.is_activated:
        raise AccountAlreadyActivated()

    background_tasks.add_task(service.create_and_send_activate_email, user=user)
    return Message(detail=SuccessMessage.SUCCESS_REQUEST_ACTIVATE_ACCOUNT)


@router.post("/users/activate")
async def activate_account(
    token: str = Body(embed=True),
    service: AuthService = Depends(get_auth_service),
) -> Message:
    await service.activate_account(token)
    return Message(detail=SuccessMessage.SUCCESS_ACTIVATE_ACCOUNT)


@router.post("/users/forgot-password")
async def forgot_password(
    background_tasks: BackgroundTasks,
    user: UserData = Depends(valid_user_email),
    service: AuthService = Depends(get_auth_service),
) -> Message:
    background_tasks.add_task(service.create_and_send_reset_password_email, user=user)
    return Message(detail=SuccessMessage.SUCCESS_REQUEST_RESET_PASSWORD)


@router.post("/users/reset-password")
async def reset_password(
    user_reset_password_data: UserResetPassword,
    service: AuthService = Depends(get_auth_service),
) -> Message:
    await service.reset_password(user_reset_password_data)
    return Message(detail=SuccessMessage.SUCCESS_RESET_PASSWORD)


@router.post("/users/tokens", response_model=TokenData)
async def login_with_normal_method(
    auth_data: AuthData,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> TokenData:
    user = await service.authenticate_user(auth_data)
    refresh_token = await service.issue_new_refresh_token(user_id=user.id)

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token.token))

    return TokenData(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token.token,
    )


@router.post("/users/tokens/google", response_model=TokenData)
async def login_via_google(
    response: Response,
    id_token: str = Body(embed=True, alias="idToken"),
    service: AuthService = Depends(get_auth_service),
) -> TokenData:
    user = await service.authenticate_user_signed_in_via_google(id_token=id_token)
    refresh_token = await service.issue_new_refresh_token(user_id=user.id)

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token.token))

    return TokenData(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token.token,
    )


@router.put("/users/tokens", response_model=TokenData)
async def refresh_tokens(
    response: Response,
    refresh_token: RefreshTokenData = Depends(valid_refresh_token),
    user: UserData = Depends(valid_refresh_token_user),
    service: AuthService = Depends(get_auth_service),
) -> TokenData:
    refresh_token = await service.issue_new_refresh_token(user_id=refresh_token.user_id)
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token.token))

    return TokenData(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token.token,
    )


@router.delete("/users/tokens", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    response: Response,
    refresh_token: RefreshTokenData = Depends(valid_refresh_token),
    service: AuthService = Depends(get_auth_service),
) -> None:
    await service.expire_refresh_token(user_id=refresh_token.user_id)
    response.set_cookie(
        **utils.get_refresh_token_settings(
            refresh_token=refresh_token.token, has_expired=True
        )
    )


@router.post("/presigned-urls/post")
async def get_presigned_url_for_uploading(
    object_name: str = Body(..., embed=True),
    jwt_data: JWTData = Depends(valid_jwt_token),
    service: AuthService = Depends(get_auth_service),
) -> PresignedUrlData:
    return await service.generate_presigned_url_post(object_name=object_name)
