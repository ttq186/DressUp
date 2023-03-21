from pydantic import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes
    JWT_EXTRA_SECRET: str

    SITE_DOMAIN: str

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True

    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str


auth_config = AuthConfig()
