from sqlalchemy import (
    ARRAY,
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
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from src.auth.constants import UserRole
from src.database import metadata

user_tb = Table(
    "user",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    ),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("password", LargeBinary),
    Column("first_name", String),
    Column("last_name", String),
    Column("avatar_url", String),
    Column("styles", ARRAY(String)),
    Column("bust", Integer),
    Column("waist", Integer),
    Column("hip", Integer),
    Column("weight", Integer),
    Column("height", Integer),
    Column("role", String, server_default=UserRole.USER, nullable=False),
    Column("is_active", Boolean, server_default="true", nullable=False),
    Column("is_activated", Boolean, server_default="false", nullable=False),
    Column("auth_method", String, server_default="NORMAL", nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    ),
)

contact_tb = Table(
    "contact",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("message", String, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    ),
)
