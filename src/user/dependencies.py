from fastapi import Depends

from src.auth.dependencies import valid_jwt_token
from src.auth.exceptions import InvalidToken
from src.auth.schemas import JWTData
from src.user.repository import UserRepo
from src.user.schemas import UserData
from src.user.service import UserService


async def get_user_service(user_repo: UserRepo = Depends()) -> UserService:
    return UserService(user_repo)


async def valid_user(
    jwt_data: JWTData = Depends(valid_jwt_token),
    user_repo: UserRepo = Depends(),
) -> UserData:
    user = await user_repo.get(id=jwt_data.user_id)
    if not user:
        raise InvalidToken()
    return user
