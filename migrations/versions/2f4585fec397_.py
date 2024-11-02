"""empty message

Revision ID: 2f4585fec397
Revises: 6d8f749d0e93
Create Date: 2024-05-21 23:32:04.924241

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2f4585fec397'
down_revision = '6d8f749d0e93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_price', sa.String(length=255), nullable=False))
        batch_op.drop_column('unit_price')
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', mysql.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('unit_price', mysql.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('product_price')

    # ### end Alembic commands ###