"""Create new_buildings table

Revision ID: ad31b5806897
Revises: 6c460bb0ad62
Create Date: 2025-06-30 17:22:44.498114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad31b5806897'
down_revision: Union[str, None] = '6c460bb0ad62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('new_buildings', sa.Column('apartment_count', sa.Integer(), nullable=True, server_default='0'))

    op.execute('UPDATE new_buildings SET apartment_count = 0 WHERE apartment_count IS NULL')

    op.alter_column('new_buildings', 'apartment_count', nullable=False, server_default=None)

def downgrade() -> None:
    op.drop_column('new_buildings', 'apartment_count')
