from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from src.database import metadata

user_tb = Table(
    "user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("is_active", Boolean, server_default="true", nullable=False),
    Column("is_activated", Boolean, server_default="false", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

refresh_token_tb = Table(
    "refresh_token",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
