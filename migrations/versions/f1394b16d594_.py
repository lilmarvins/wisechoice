"""empty message

Revision ID: f1394b16d594
Revises: 9e8a5d07f416
Create Date: 2024-05-21 23:51:23.897759

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f1394b16d594'
down_revision = '9e8a5d07f416'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Text(), nullable=False))
        batch_op.drop_column('product_price')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', mysql.TEXT(), nullable=False))

    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_price', mysql.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
