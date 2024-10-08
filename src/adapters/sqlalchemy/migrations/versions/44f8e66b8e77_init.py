"""init

Revision ID: 44f8e66b8e77
Revises: 
Create Date: 2024-08-09 01:54:59.232073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44f8e66b8e77'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('walker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('walk_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('apartment_number', sa.Integer(), nullable=True),
    sa.Column('dog_name', sa.String(), nullable=True),
    sa.Column('dog_breed', sa.String(), nullable=True),
    sa.Column('walk_date', sa.Date(), nullable=True),
    sa.Column('walk_time', sa.Time(), nullable=True),
    sa.Column('walk_duration', sa.Integer(), nullable=True),
    sa.Column('walker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['walker_id'], ['walker.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('walk_order')
    op.drop_table('walker')
    # ### end Alembic commands ###
