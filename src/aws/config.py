from pydantic import BaseSettings


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_IMAGE_BUCKET: str
    AWS_PRESIGNED_URL_EXPIRE_SECONDS: int


settings = Settings()
