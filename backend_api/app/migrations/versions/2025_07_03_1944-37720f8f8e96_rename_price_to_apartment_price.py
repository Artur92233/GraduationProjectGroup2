"""rename price to apartment_price

Revision ID: 37720f8f8e96
Revises: c3daa786b71e
Create Date: 2025-07-03 19:44:54.131015

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "37720f8f8e96"
down_revision: Union[str, None] = "c3daa786b71e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("new_buildings", "price", new_column_name="apartment_price")


def downgrade() -> None:
    op.alter_column("new_buildings", "apartment_price", new_column_name="price")
