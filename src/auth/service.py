from datetime import timedelta
from uuid import UUID

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

from src import utils
from src.auth import jwt
from src.auth.config import settings
from src.auth.constants import AuthMethod
from src.auth.exceptions import (
    AccountNotActivated,
    AccountSuspended,
    InvalidCredentials,
    InvalidToken,
    AccountCreatedViaThirdParty,
    AccountCreatedByNormalMethod,
)
from src.auth.repository import AuthRepo
from src.auth.schemas import (
    AuthData,
    RefreshTokenCreate,
    RefreshTokenData,
    RefreshTokenUpdate,
    UserResetPassword,
)
from src.auth.security import check_password
from src.auth.utils import send_activate_email, send_reset_password_email
from src.user.repository import UserRepo
from src.user.schemas import UserCreate, UserData
from src.utils import logger, utc_now


class AuthService:
    def __init__(self, auth_repo: AuthRepo, user_repo: UserRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def authenticate_user(self, auth_data: AuthData) -> UserData:
        user = await self.user_repo.get_by_email(auth_data.email)

        if not user or not await check_password(auth_data.password, user.password):
            raise InvalidCredentials()

        if user.auth_method != AuthMethod.NORMAL:
            raise AccountCreatedViaThirdParty()

        if not user.is_active:
            raise AccountSuspended()

        if not user.is_activated:
            raise AccountNotActivated()
        return user

    async def authenticate_user_signed_in_via_google(self, id_token: str) -> UserData:
        try:
            id_info = verify_oauth2_token(id_token=id_token, request=requests.Request())

            user = await self.user_repo.get_by_email(id_info["email"])
            if not user:
                create_data = UserCreate(
                    email=id_info["email"],
                    auth_method=AuthMethod.GOOGLE,
                    first_name=id_info["given_name"],
                    last_name=id_info["family_name"],
                    is_activated=True,
                    is_active=True,
                )
                user = await self.user_repo.create(create_data)

            if user.auth_method != AuthMethod.GOOGLE:
                raise AccountCreatedByNormalMethod()

            if not user.is_active:
                raise AccountSuspended()
            return user
        except Exception as e:
            logger.warning(f"Decode oauth2: {e}")
            raise InvalidToken()

    async def create_refresh_token(self, user_id: UUID) -> RefreshTokenData:
        create_data = RefreshTokenCreate(
            user_id=user_id,
            token=utils.generate_random_alphanum(64),
            expires_at=utc_now()
            + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES_SECONDS),
        )
        return await self.auth_repo.create_refresh_token(create_data=create_data)

    async def issue_new_refresh_token(self, user_id: UUID) -> RefreshTokenData:
        update_data = RefreshTokenUpdate(
            token=utils.generate_random_alphanum(64),
            expires_at=utc_now()
            + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES_SECONDS),
        )
        return await self.auth_repo.update_refresh_token(
            user_id=user_id, update_data=update_data
        )

    async def expire_refresh_token(self, user_id: UUID):
        update_data = RefreshTokenUpdate(
            user_id=user_id, expires_at=utc_now() - timedelta(days=1)
        )
        return await self.auth_repo.update_refresh_token(
            user_id=user_id, update_data=update_data
        )

    def create_and_send_activate_email(self, user: UserData) -> None:
        username = user.full_name or user.email.split("@")[0]
        token = jwt.create_access_token(
            user=user,
            expires_delta=timedelta(minutes=15),
            secret_key=settings.JWT_EXTRA_SECRET,
        )
        activate_url = f"{settings.SITE_DOMAIN}/users/activate?token={token}"
        send_activate_email(
            receiver_email=user.email,
            username=username,
            activate_url=activate_url,
        )

    def create_and_send_reset_password_email(self, user: UserData) -> None:
        username = user.full_name or user.email.split("@")[0]
        token = jwt.create_access_token(
            user=user,
            expires_delta=timedelta(minutes=10),
            secret_key=settings.JWT_EXTRA_SECRET,
        )
        reset_url = f"{settings.SITE_DOMAIN}/users/reset-password?token={token}"
        send_reset_password_email(
            receiver_email=user.email,
            username=username,
            reset_url=reset_url,
        )

    async def reset_password(self, user_reset_password_data: UserResetPassword) -> None:
        token_data = jwt.decode_token(
            token=user_reset_password_data.token, secret_key=settings.JWT_EXTRA_SECRET
        )
        await self.user_repo.update_user(
            id=token_data["id"],
            update_data={"password": user_reset_password_data.new_password},
        )

    async def activate_account(self, token: str) -> None:
        token_data = jwt.decode_token(token=token, secret_key=settings.JWT_EXTRA_SECRET)
        await self.user_repo.update_user(
            id=token_data["id"], update_data={"is_activated": True}
        )
