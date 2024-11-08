"""empty message

Revision ID: 5c83ce72cc11
Revises: 4645646f18eb
Create Date: 2024-05-26 21:28:46.236394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c83ce72cc11'
down_revision = '4645646f18eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ip_address', sa.String(length=250), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('ip_address')

    # ### end Alembic commands ###
