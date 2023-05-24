from datetime import timedelta

import boto3

from src.aws.config import settings
from src.utils import utc_now


class S3:
    def __init__(
        self,
        access_key_id: str = settings.AWS_ACCESS_KEY_ID,
        secret_access_key: str = settings.AWS_SECRET_ACCESS_KEY,
    ):
        self._client = boto3.client(
            "s3",
            region_name="ap-southeast-1",  # Singapore region
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )

    def generate_presigned_url_post(
        self, object_name: str, bucket_name: str = settings.AWS_DEFAULT_IMAGE_BUCKET
    ) -> dict:
        response = self._client.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_name,
            ExpiresIn=settings.AWS_PRESIGNED_URL_EXPIRE_SECONDS,
        )
        response["expires_at"] = utc_now() + timedelta(
            seconds=settings.AWS_PRESIGNED_URL_EXPIRE_SECONDS
        )
        return response
