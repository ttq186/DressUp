from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func, text
from sqlalchemy.dialects.postgresql import UUID

from src.database import metadata

refresh_token_tb = Table(
    "refresh_token",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    ),
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=True,
    ),
    Column("token", String, nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)
