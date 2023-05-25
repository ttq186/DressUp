"""added_user_role_field

Revision ID: 338bae562a5b
Revises: 2a6fa26476b5
Create Date: 2023-05-25 09:11:58.207495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "338bae562a5b"
down_revision = "2a6fa26476b5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("role", sa.String(), server_default="USER", nullable=False)
    )
    op.drop_column("user", "is_admin")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "is_admin",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("user", "role")
    # ### end Alembic commands ###
