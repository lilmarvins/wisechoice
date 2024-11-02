"""empty message

Revision ID: df961fc9c2b8
Revises: 
Create Date: 2024-05-04 01:42:30.358912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df961fc9c2b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('cat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cat_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('date_reg', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('pending,sold,canceled'), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('products',
    sa.Column('prod_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('prod_name', sa.String(length=100), nullable=False),
    sa.Column('prod_description', sa.Text(), nullable=False),
    sa.Column('prod_price', sa.String(length=255), nullable=False),
    sa.Column('prod_quantity', sa.String(length=255), nullable=False),
    sa.Column('prod_image', sa.String(length=100), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.cat_id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('prod_id')
    )
    op.create_table('review',
    sa.Column('review_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('review_text', sa.Text(), nullable=False),
    sa.Column('review_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('review_id')
    )
    op.create_table('transaction',
    sa.Column('transaction_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Text(), nullable=False),
    sa.Column('amount', sa.String(length=255), nullable=False),
    sa.Column('transaction_date', sa.DateTime(), nullable=True),
    sa.Column('transactiion_ststus', sa.Enum('pending,canceled,completed'), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    op.create_table('order_items',
    sa.Column('order_item_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Text(), nullable=False),
    sa.Column('unit_price', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.prod_id'], ),
    sa.PrimaryKeyConstraint('order_item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('transaction')
    op.drop_table('review')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###
