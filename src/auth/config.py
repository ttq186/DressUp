from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXPIRES_SECONDS: int
    JWT_EXTRA_SECRET: str

    SITE_DOMAIN: str

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXPIRES_SECONDS: int

    SECURE_COOKIES: bool = True

    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str


settings = Settings()
