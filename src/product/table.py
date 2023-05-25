from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
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

product_tb = Table(
    "product",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column(
        "owner_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    ),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("brand", String),
    Column("is_public", Boolean),
    Column("material", String),
    Column("style", String),
    Column("pattern", String),
    Column("shop_id", BigInteger),
    Column("original_url", String),
    Column("shopee_affiliate_url", String),
    Column("lazada_affiliate_url", String),
    Column("tiktok_affiliate_url", String),
    Column("transparent_background_image", String),
    Column("image_urls", ARRAY(String)),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

category_tb = Table(
    "category",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("display_name", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

product_category_tb = Table(
    "product_category",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column(
        "product_id",
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column(
        "category_id",
        ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
)


product_rating_tb = Table(
    "product_rating",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column(
        "product_id",
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("score", Integer, nullable=False),
)

product_review_tb = Table(
    "product_review",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column(
        "product_id",
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("content", String),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)
