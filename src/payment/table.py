from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Table,
    func,
)

from src.database import metadata

subscription = Table(
    "subscription",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Integer, nullable=False),
    Column("billing_period_in_days", Integer, nullable=False),
)


payment_history = Table(
    "payment_history",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "subscription_id",
        ForeignKey("subscription.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("price", Integer, nullable=False),
    Column("status", String, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
)
