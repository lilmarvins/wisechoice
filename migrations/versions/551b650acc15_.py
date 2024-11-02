"""empty message

Revision ID: 551b650acc15
Revises: 12d7704ff624
Create Date: 2024-05-24 09:47:49.174000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '551b650acc15'
down_revision = '12d7704ff624'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.alter_column('transaction_status',
               existing_type=mysql.ENUM('pending,canceled,completed'),
               type_=sa.Enum('pending', 'canceled', 'completed'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.alter_column('transaction_status',
               existing_type=sa.Enum('pending', 'canceled', 'completed'),
               type_=mysql.ENUM('pending,canceled,completed'),
               existing_nullable=True)

    # ### end Alembic commands ###