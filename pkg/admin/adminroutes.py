from functools import wraps
from flask import render_template, request, redirect, flash, make_response, session,abort
from markupsafe import escape
from flask_wtf.csrf import CSRFError
from werkzeug.security import generate_password_hash, check_password_hash
import os,secrets
from . import adminobj
from pkg.error.error import errorbp

from pkg.models import db,Admin,User,Products,Category,Orders,Transaction


def get_user_by_id(id):
    deets= db.session.query(Admin).get(id)
    return deets




def login_required(f):
    @wraps(f)
    def check_login(*args,**kwargs):
        if session.get('adminonline') != None:
            return f(*args,**kwargs)
        else:
            flash('you must be logged in to access this page', category='error')
            return redirect ('/home/login/')
    return check_login



@adminobj.route('/adminuser/', methods=['POST','GET'])
@login_required
def adminuser():
    id = session.get('adminonline')
    admin = get_user_by_id(id)
    admindets= Admin.query.all()
    return render_template('admin.html',admin=admin, admindets=admindets,title='admin users')




@adminobj.route('/allorders/',methods=['POST','GET'])
@login_required
def allorders():
    id = session.get('adminonline')
    admin = get_user_by_id(id)
    orders= Orders.query.all()
    return render_template('order.html',admin=admin,orders=orders)




@adminobj.route('/allpayment/',methods=['POST','GET'])
@login_required
def allpayments():
    id = session.get('adminonline')
    admin = get_user_by_id(id)
    payment= Transaction.query.all()
    return render_template('payment.html',admin=admin,payment=payment)







@adminobj.route('/addprod/',methods=['POST','GET'])
@login_required
def addprod():
    id = session.get('adminonline')
    admin = get_user_by_id(id)
    cat = Category.query.all()
    if request.method == "GET":
       
        return render_template('addproduct.html', cat=cat,admin=admin, title='add product')
    else:
        prod_desc= request.form.get('product')
        prod_name = request.form.get('prod_name')
        prod_cat= request.form.get('prod_cat')
        prod_quantity= request.form.get('prodamount')
        prod_price= request.form.get('prodprice')
        prod_file= request.files.get('file')
        filename = prod_file.filename
        allowed_ext=[".jpg",".png",".jpeg"]
        
        if filename:
            ext= os.path.splitext(filename)[-1]
            if ext in allowed_ext:                
                new_file=secrets.token_hex(7)+ ext
                prod_file.save("pkg/static/images/"+new_file)
                products= Products(category_id=prod_cat,prod_name=prod_name,prod_description=prod_desc,prod_quantity=prod_quantity,prod_image=new_file,prod_price=prod_price)
                
                db.session.add(products)
                db.session.commit()
                flash('Product Uploaded successfully', category='success')
                return redirect('/admin/allproducts/')
            else:
                flash('FIle extension not supported, allowed extensions are jpg,png and jpeg', category='error')
                return redirect('/admin/addprod/')
        else:
            flash("you need to selest a file for upload")
            return redirect("/admin/addprod/")





@adminobj.route('/addcategory/',methods=['POST','GET'])
@login_required
def addcategory():
    id = session.get('adminonline')
    admin = get_user_by_id(id)
    catname = request.form.get('prod_cat')
    catimg = request.files.get('catimg')
    cat = Category.query.all()
    if request.method == 'GET':
        return render_template('addcategory.html',cat=cat,admin=admin,title='add category')
    else:
       filename = catimg.filename
       allowed_ext=[".jpg",".png",".jpeg"]
        
       if filename:
            ext= os.path.splitext(filename)[-1]
            if ext in allowed_ext:                
                new_file=secrets.token_hex(7)+ ext
                catimg.save("pkg/static/images/"+new_file)
                category = Category(cat_name=catname,cat_image=new_file)
                db.session.add(category)
                db.session.commit()
                flash('category successfully added',category='success')
                return redirect(request.referrer)
            else:
                flash('FIle extension not supported, allowed extensions are jpg,png and jpeg', category='error')
                
                return redirect(request.referrer)


@adminobj.route('/catedit/<int:id>/',methods=['POST','GET'])
@login_required
def catedit(id):
    ids = session.get('adminonline')
    admin = get_user_by_id(ids)
    catname = request.form.get('prod_cat')
    catimg = request.files.get('catimg')
    cat = Category.query.filter(Category.cat_id==id)
    if request.method == "GET":
        return render_template('catedit.html',admin=admin,cat=cat)
    else:
        filename = catimg.filename
        allowed_ext=[".jpg",".png",".jpeg"]
        
        if filename:
            ext= os.path.splitext(filename)[-1]
            if ext in allowed_ext:                
                new_file=secrets.token_hex(7)+ ext
                catimg.save("pkg/static/images/"+new_file)
                category = Category.query.get(id)
                category.cat_name=catname
                category.cat_image=new_file
                db.session.commit() 
                flash('category successfully updated',category='success')
                return redirect('/admin/addcategory/')
            else:
                flash('FIle extension not supported, allowed extensions are jpg,png and jpeg', category='error')
                return redirect(request.referrer)




@adminobj.route('/createadmin/', methods=['POST','GET'])
@login_required
def createadmin():
    admin_name = request.form.get('admin_name')
    admin_email= request.form.get('admin_email')
    admin_pwd= request.form.get('admin_pwd')
    if admin_name != "" and admin_email != "" and admin_pwd != "":
         hashed = generate_password_hash(admin_pwd)
         admin= Admin(admin_email=admin_email,admin_username=admin_name,admin_password=hashed)
         db.session.add(admin)
         db.session.commit()
         flash(f'admin {admin_name} successfully created')
         return redirect('/admin/adminuser/')
    else:
        flash('all fields required',category='error')
        return redirect('/admin/adminuser/')
    


@adminobj.route('/deleteadmin/<int:id>', methods=['POST','GET'])
def deleteadmin(id):
    admin = db.session.query(Admin).get(id)
    db.session.delete(admin)
    db.session.commit()
    return redirect('/admin/adminuser/')



@adminobj.route('/deletecat/<int:id>/', methods=['POST','GET'])
def deletecat(id):
    cat = db.session.query(Category).get(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect('/admin/addcategory/')




@adminobj.route('/', methods=['POST','GET'])
def adminlogin():

    if request.method == 'GET':
         return render_template('adminlogin.html')
    else:
        email = request.form.get('adminemail')
        pwd = request.form.get('adminpwd')
        if email == '' or pwd =='':
            flash('Both fields must be supplied', category='error')
            return redirect("/admin/")
        else:
            admin = db.session.query(Admin).filter(Admin.admin_email==email).first()
            if admin != None:
                stored_hash= admin.admin_password
                chk = check_password_hash(stored_hash,pwd)
                if chk == True:
                    session['adminonline'] = admin.admin_id
                    return redirect("/admin/dashboard/")
                else:
                    flash('invalid password',category= 'error' )
                    return redirect("/admin/")
            else:
                    flash('invalid email', category= 'error')
            return redirect("/admin/")
        
    
@adminobj.route('/users/', methods=['POST','GET'])
@login_required
def users():
    id = session.get('adminonline')
    admin = get_user_by_id(id) 
    if request.method == 'GET':
        Duser= User.query.all()
    return render_template('users.html',admin=admin,Duser=Duser,title="List Of Users")
        
    
@adminobj.route('/allproducts/', methods=['POST','GET'])
@login_required
def allproducts():
    id = session.get('adminonline')
    admin = get_user_by_id(id) 
    products = Products.query.all()
    return render_template('breakout.html',admin=admin,products=products,title='alll products')






@adminobj.route('/dashboard/', methods=['POST','GET'])
@login_required
def admindashboard():
    id = session.get('adminonline')
    admin = get_user_by_id(id) 
    if request.method == 'GET':
        Duser= User.query.all()
        return render_template('dashboard.html',admin=admin,Duser=Duser,title="admin dashboard")
    
@adminobj.route('/deleteuser/<int:id>')
def deleteuser(id):
    user = db.session.query(User).get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin/dashboard/')

@adminobj.route('/deleteprod/<int:id>')
def deleteprod(id):
    prod = db.session.query(Products).get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/admin/allproducts/')





@adminobj.route('/adminsetting/',methods=['POST',"GET"])
@login_required
def adminsetting():
    id = session.get('adminonline')
    admin = get_user_by_id(id) 
    if request.method== "GET":
        return render_template('adminsetting.html',admin=admin,title='admin settings')
    else:
        admin_email= request.form.get('admin_email')
        admin_password= request.form.get('admin_password')
        username= request.form.get('username')
        hashed = generate_password_hash(admin_password)
        admin.admin_email=admin_email
        admin.admin_username = username
        admin.admin_password= hashed
        db.session.commit()
        return redirect('/admin/adminsetting')








@adminobj.route('/logout/')
def logout():
    if session.get("adminonline"):
        session.pop('adminonline')
    return redirect('/admin/')







@errorbp.app_errorhandler(404)
def page_not(error):
    id = session.get('adminonline')
    if id != None:
        admin = get_user_by_id(id)
    return render_template('pagenotfound.html',admin=admin),404







@adminobj.after_request
def fun_after_request(response):

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@adminobj.route('/layout/')
def layout():
    id = session.get('adminonline')
    admin = Admin.query.get(id)
    return render_template("admin_layout.html", admin=admin)