"""Update db

Revision ID: 73cd62f1b242
Revises: 43ee5385a51d
Create Date: 2023-12-14 15:04:26.988504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '73cd62f1b242'
down_revision: Union[str, None] = '43ee5385a51d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('permissions', sa.JSON(), nullable=True))
    op.drop_column('role', 'permissons')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('permissons', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('role', 'permissions')
    # ### end Alembic commands ###
