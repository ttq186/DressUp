"""remove_product_rating_score

Revision ID: 177cf327b079
Revises: acf2fa2bcf67
Create Date: 2023-05-26 14:43:55.049871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "177cf327b079"
down_revision = "acf2fa2bcf67"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_rating", "score")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product_rating",
        sa.Column("score", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###