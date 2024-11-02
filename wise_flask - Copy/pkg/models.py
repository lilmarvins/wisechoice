from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    user_image=db.Column(db.String(50))
    username = db.Column(db.String(100), nullable=False,index=True)
    email= db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable= False)
    address = db.Column(db.String(250))
    city= db.Column(db.String(250))
    state= db.Column(db.String(250))
    zip =db.Column(db.String(250))
    phone_number = db.Column(db.String(15))
    date_reg= db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#set relationship
    my_order = db.relationship("Orders", back_populates="my_user")
    user_seller = db.relationship('Products', back_populates="seller_user")
    user_trans = db.relationship("Transaction", back_populates="trans_user")


class Orders(db.Model):
    order_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    buyer_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    order_date= db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum("pending","confirmed","failed"))
    ip_address= db.Column(db.String(250))
# set relationship
    my_user = db.relationship("User", back_populates="my_order")
    semi_order_deets = db.relationship('Order_items', back_populates="order_items_deets")





class Products(db.Model):
    prod_id =  db.Column(db.Integer,autoincrement=True, primary_key=True)
    seller_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    category_id = db.Column(db.Integer,db.ForeignKey("category.cat_id"))
    prod_name = db.Column(db.String(200), nullable=False, index=True)
    prod_description= db.Column(db.Text, nullable=False)
    prod_price= db.Column(db.String(255), nullable=False)
    prod_quantity= db.Column(db.String(255), nullable=False)
    prod_image= db.Column(db.String(100), nullable=False)
    date_added= db.Column(db.DateTime, default=datetime.utcnow)
    # set relationship
    order_deets = db.relationship('Order_items', back_populates="prod_deets")
    prod_cat = db.relationship('Category', back_populates="cat_prod")
    seller_user = db.relationship('User', back_populates="user_seller")

class Category(db.Model):
    cat_id= db.Column(db.Integer,autoincrement=True, primary_key=True)
    cat_image = db.Column(db.String(250), nullable=True)
    cat_name = db.Column(db.String(100), nullable=False,index=True)

    # set relationship
    cat_prod = db.relationship('Products', back_populates="prod_cat")


class Review(db.Model):
    review_id= db.Column(db.Integer,autoincrement=True, primary_key=True)
    seller_id= db.Column(db.Integer,db.ForeignKey("user.user_id"))
    buyer_id=  db.Column(db.Integer,db.ForeignKey("user.user_id"))
    review_text=  db.Column(db.Text, nullable=False)
    review_date= db.Column(db.DateTime, default=datetime.utcnow)

class Order_items(db.Model):
    order_item_id= db.Column(db.Integer,autoincrement=True, primary_key=True)
    order_id= db.Column(db.Integer,db.ForeignKey("orders.order_id"))
    product_id= db.Column(db.Integer,db.ForeignKey("products.prod_id"))
    buyer_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    # set relationship
    prod_deets = db.relationship('Products', back_populates="order_deets")
    order_items_deets = db.relationship('Orders', back_populates="semi_order_deets")


class Transaction(db.Model):
    transaction_id= db.Column(db.Integer,autoincrement=True, primary_key=True)
    buyer_id=  db.Column(db.Integer,db.ForeignKey("user.user_id"))
    amount= db.Column(db.String(255), nullable=False)
    serial_number= db.Column(db.String(255), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_status= db.Column(db.Enum("pending","failed","completed"))
#   set relationship
    trans_user = db.relationship("User", back_populates="user_trans")

class Admin(db.Model):
    admin_id= db.Column(db.Integer,autoincrement=True, primary_key=True)
    admin_email = db.Column(db.String(200), nullable=False, index=True, unique=True)
    admin_username = db.Column(db.String(200), nullable=False)
    admin_password = db.Column(db.String(200), nullable=False)
    admin_created_on = db.Column(db.DateTime, default=datetime.utcnow)
    admin_lastlogged = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)