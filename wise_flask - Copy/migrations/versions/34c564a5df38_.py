"""empty message

Revision ID: 34c564a5df38
Revises: 469f847a5f80
Create Date: 2024-05-07 06:31:48.084455

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '34c564a5df38'
down_revision = '469f847a5f80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_email', sa.String(length=200), nullable=False),
    sa.Column('admin_username', sa.String(length=200), nullable=False),
    sa.Column('admin_password', sa.String(length=200), nullable=False),
    sa.Column('admin_lastlogged', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('admin_id')
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_admin_email'), ['admin_email'], unique=True)

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('prod_name',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('prod_name',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_admin_email'))

    op.drop_table('admin')
    # ### end Alembic commands ###
