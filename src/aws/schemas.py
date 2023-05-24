from datetime import datetime

from src.schemas import BaseModel


class PresignedUrlData(BaseModel):
    url: str
    fields: dict
    expires_at: datetime
