from databases.interfaces import Record
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from src.auth import exceptions, jwt, service, utils
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user,
    valid_user_create,
)
from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import (
    AccessTokenResponse,
    AuthUser,
    JWTData,
    User,
    UserActivate,
    UserResetPassword,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_create),
) -> dict[str, str]:
    user = await service.create_user(auth_data)
    return user  # type: ignore


@router.post("/users/activate/request")
async def request_activate_account(
    background_tasks: BackgroundTasks,
    user: User = Depends(valid_user),
) -> dict[str, str]:
    if user.is_activated:
        raise exceptions.AccountAlreadyActivated()

    background_tasks.add_task(service.create_and_send_activate_email, user=user)
    return {
        "detail": "An activate link has just been sent. Please check your email box!"
    }


@router.post("/users/activate")
async def activate_account(user_activate_payload: UserActivate) -> dict[str, str]:
    await service.activate_account(user_activate_payload)
    return {"detail": "Your account has been activated! Please sign in again!"}


@router.post("/users/forgot-password")
async def forgot_password(
    background_tasks: BackgroundTasks,
    user: User = Depends(valid_user),
) -> dict[str, str]:
    background_tasks.add_task(service.create_and_send_reset_password_email, user=user)
    return {
        "detail": "An activate link has just been sent. Please check your email box!"
    }


@router.post("/users/reset-password")
async def reset_password(
    user_reset_payload: UserResetPassword,
) -> dict[str, str]:
    await service.reset_password(user_reset_payload)
    return {"detail": "Your password has been reset successfully!"}


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user = await service.get_user_by_id(jwt_data.user_id)
    return user  # type: ignore


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(auth_data: AuthUser, response: Response) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    background_tasks: BackgroundTasks,
    response: Response,
    refresh_token: Record = Depends(valid_refresh_token),
    user: Record = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    background_tasks.add_task(service.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: Record = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["token"], expired=True)
    )
