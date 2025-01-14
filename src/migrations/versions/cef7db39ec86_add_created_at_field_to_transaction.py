"""add created_at field to transaction

Revision ID: cef7db39ec86
Revises: f1e4f2b3eb7b
Create Date: 2024-09-16 19:00:25.824315

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cef7db39ec86"
down_revision: Union[str, None] = "f1e4f2b3eb7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "transaction",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("transaction", "created_at")
    # ### end Alembic commands ###
