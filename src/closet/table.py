from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    Table,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from src.database import metadata

closet_tb = Table(
    "closet",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    ),
    Column(
        "owner_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)


closet_item_tb = Table(
    "closet_item",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column(
        "closet_id",
        ForeignKey("closet.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("product_id", ForeignKey("product.id", ondelete="CASCADE"), nullable=False),
    UniqueConstraint("closet_id", "product_id"),
)
