from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Float,
    Identity,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)

from src.database import metadata

user_tb = Table(
    "user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("first_name", String),
    Column("last_name", String),
    Column("avatar_url", String),
    Column("password", LargeBinary),
    Column("styles", ARRAY(String)),
    Column("burst", Integer),
    Column("waist", Integer),
    Column("hip", Integer),
    Column("weight", Float),
    Column("height", Float),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("is_active", Boolean, server_default="true", nullable=False),
    Column("is_activated", Boolean, server_default="false", nullable=False),
    Column("auth_method", String, server_default="NORMAL", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
