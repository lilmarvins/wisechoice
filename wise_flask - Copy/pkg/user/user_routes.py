from functools import wraps
from flask import render_template, request, redirect, flash, make_response, session,abort,jsonify
from markupsafe import escape
from flask_wtf.csrf import CSRFError
from werkzeug.security import generate_password_hash, check_password_hash
import json,os,secrets,requests,random,string,os,json
from datetime import datetime

from . import userobj
from pkg.error.error import errorbp
from pkg.models import db,User,Products,Category,Order_items,Orders,Transaction


def get_user_by_id(id):
    deets= db.session.query(User).get(id)
    return deets


def login_required(f):
    @wraps(f)
    def check_login(*args,**kwargs):
        if session.get('useronline') != None:
            return f(*args,**kwargs)
        else:
            flash('you must be logged in to access this page', category='error')
            return redirect ('/home/login/')
    return check_login



       
   
    





@userobj.route('/')
def landingpage():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    products = Products.query.all()
    cat= Category.query.all()
    return render_template('user/index.html',userdets=userdets,products=products,cat=cat)


# @userobj.route('/search/')






@userobj.errorhandler(CSRFError)
def csrf_error_handler(e):
    return render_template('user/csrf_error.html',err=e.description), 400



@userobj.route('/homepage/', methods=['GET','POST'])
@login_required
def home():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    products = Products.query.all()
    cat= Category.query.all()
    return render_template('user/indexlogged.html', userdets=userdets,products=products,cat=cat)
  
    


@userobj.route('/orders/')
@login_required
def orders():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    order = Order_items.query.filter(Order_items.buyer_id==id)
    return render_template('user/order.html', userdets=userdets,order=order)
 

    

@userobj.route('/terms/')
def terms():
    return render_template('user/terms.html')

@userobj.route('/settings/')
@login_required
def settings():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    return render_template('user/settings.html', userdets=userdets)

   


@userobj.route('/produpload/',methods=["GET",'POST'])
@login_required
def produpload():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    if request.method == "GET":
        
        cat = Category.query.all()
        return render_template('user/produpload.html', userdets=userdets,cat=cat)
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
                products= Products(seller_id=userdets.user_id,category_id=prod_cat,prod_name=prod_name,prod_description=prod_desc,prod_quantity=prod_quantity,prod_image=new_file,prod_price=prod_price)
                
                db.session.add(products)
                db.session.commit()
                flash('Product Uploaded successfully', category='success')
                return redirect('/home/my_products/')
            else:
                flash('FIle extension not supported, allowed extensions are jpg,png and jpeg', category='error')
                return redirect('/home/produpload/')
        else:
            flash("you need to selest a file for upload")
            return redirect("/home/produpload/")


@userobj.route('/my_products/', methods=['GET','POST'])
@login_required
def my_products():
    image = request.form.get('photo')
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    product = Products.query.all()
    prod = Products.query.filter(Products.seller_id==id).count()
    user_file= request.files.get('photo')
    if request.method == "GET":
        return render_template('user/my_products.html', userdets=userdets,product=product,prod=prod)
    else:
        filename = user_file.filename
        allowed_ext=[".jpg",".png",".jpeg"]
        ext= os.path.splitext(filename)[-1]
        if ext in allowed_ext:                
            new_file=secrets.token_hex(7)+ ext
            old_img = userdets.user_image
            user_file.save("pkg/static/images/"+new_file)
            userdets.user_image=new_file
            db.session.commit()
            flash ('image have been uploaded')
            return redirect (request.referrer)





@userobj.route('/prod_edit/<int:id>', methods=['Get','POST'])
@login_required
def prod_edit(id):
    ids= session.get('useronline')
    userdets= get_user_by_id(ids)
    cat = Category.query.all()
    prodid=  request.form.get("prodid")
    products = Products.query.get(id) 
    if request.method == 'GET':
        return render_template('user/prod_edit.html', userdets=userdets,products=products,cat=cat)

    else:
        prod_desc= request.form.get('product')
        prod_name = request.form.get('prod_name')
        prod_cat= request.form.get('prod_cat')
        prod_quantity= request.form.get('prodamount')
        prod_price= request.form.get('prodprice')
        prod_file= request.files.get('file')
        
        filename = prod_file.filename
        allowed_ext=[".jpg",".png",".jpeg"]
        ext= os.path.splitext(filename)[-1]
        
        if ext in allowed_ext:                
            new_file=secrets.token_hex(7)+ ext
            old_img = products.prod_image
            os.remove("pkg/static/images/"+old_img)
            prod_file.save("pkg/static/images/"+new_file)
            products.category_id=prod_cat
            products.prod_name=prod_name
            products.prod_description=prod_desc
            products.prod_quantity=prod_quantity
            products.prod_image=new_file
            products.prod_price=prod_price
            db.session.commit()
            flash("Product Edited Successfully",category="success")
            return redirect('/home/my_products/')
        else:
            return render_template('user/prod_edit.html', userdets=userdets)

@userobj.route('/delete/<int:id>/')
@login_required
def delete(id):
    ids = session.get('useronline')
    prod_delete= db.session.query(Products).get(id)
    prod_delete_img= prod_delete.prod_image
    os.remove("pkg/static/images/"+prod_delete_img)
    db.session.delete(prod_delete)
    db.session.commit()
    return redirect('/home/my_products/')














@userobj.route('/proddeets/<int:id>/')

def prod_deets(id):
    ids= session.get('useronline')
    userdets= get_user_by_id(ids)
    products= Products.query.filter(Products.prod_id==id)  
    return render_template("user/prod_deets.html" ,userdets=userdets,products=products)




@userobj.route('/catdeets/<int:id>/')
def cat_deets(id):
    ids= session.get('useronline')
    userdets= get_user_by_id(ids)
    cat= Category.query.get(id) 
    products = cat.cat_prod 
    return render_template("user/catdeets.html" ,userdets=userdets,cat=cat,products=products)







@userobj.route('/login/', methods=['GET','POST'])
def login():
   if request.method == 'GET':
        return render_template('user/login.html')
   else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        if email == '' or pwd =='':
            flash('Both fields must be supplied', category='error')
            return redirect("/home/login/")
        else:
            user = db.session.query(User).filter(User.email==email).first()
            if user != None :
                stored_hash= user.password
                chk = check_password_hash(stored_hash,pwd)
                if chk == True:
                    
                    session['useronline'] = user.user_id
                    return redirect("/home/homepage/")
                else:
                    flash('invalid password',category= 'error' )
            else:
                    flash('invalid email', category= 'error')
            return redirect("/home/login/")
        


@userobj.route('/register/', methods=['GET','POST'])
def register():
  if request.method == 'GET':
        return render_template('user/login.html')
  else:
        name= request.form.get('username')
        emailsign= request.form.get("emailsign")
        password= request.form.get('Passwordsign')
        hashed = generate_password_hash(password)
        user = User(username=name,email=emailsign,password=hashed)
        db.session.add(user)
        db.session.commit()
        userid= user.user_id
        session['useronline']= userid
        return redirect("/home/homepage/")
        
        
def MagerDict(dict1,dict2):
    if isinstance(dict, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@userobj.route('/addcart/' , methods=['POST'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity= request.form.get('quantity')
        product = Products.query.filter_by(prod_id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DictItems={product_id:{'name':product.prod_name,'price':product.prod_price,'quantity':quantity, 'image':product.prod_image}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key,item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            print('ok')
                            
                else:
                    session['Shoppingcart']= MagerDict(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart']= DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)



@userobj.route("/cart/")
@login_required
def cart():
    ids= session.get('useronline')
    userdets= get_user_by_id(ids)
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal= 0
    grandtotal= 0
    for key, product in session["Shoppingcart"].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax=("%.2f" %(.06* float(subtotal) ))
        grandtotal= float("%.2f"%(1 * subtotal)) 
        session['grandtotal']=grandtotal
    return render_template ("user/cart.html" ,userdets=userdets,grandtotal=grandtotal)


@userobj.route("/updatecart/<int:code>/", methods=["POST"])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session["Shoppingcart"]) <= 0:
        return redirect('/home/homepage/') 
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified= True
            if quantity != "":
                for key,item in session['Shoppingcart'].items():
                    if int(key) == code:
                        item['quantity'] = quantity
                        flash('Item have been updated')
                        return redirect('/home/cart/')
            else:
                flash("quantity cannot be empty" , category='error')
                return redirect('/home/cart/')
            
        except Exception as e:
            print(e)
            flash("quantity cannot be empty" , category='error')
            return redirect('/home/cart/')


@userobj.route('/clearcart/',methods=['POST','GET'])
def clearcart():
    session.pop('Shoppingcart')
    return redirect('/home/homepage/')
   






@userobj.route('/profile_edit/')






@userobj.route("/paystack/initialize/", methods=['POST','Get'])
def paystack_initialize():
    ref = session.get("payref")
    id = session.get('useronline')
    userdets = get_user_by_id(id)
    if ref!= None:
        paydeets= Transaction.query.filter(Transaction.serial_number==ref).first()
        total = session.get('grandtotal')
        email= userdets.email
        callback_url="http://127.0.0.1:5020/home/pay/landing/"
        headers= {"Content-Type":"application/json",
                  "Authorization": "Bearer sk_test_22401be45dc31477f629d7ab5b95924fe9318d4f"
                  }
        url= "https://api.paystack.co/transaction/initialize"
        data= {"amount":total, "email":email,"reference": ref, "callback_url":callback_url}
        try:
            response = requests.post(url,headers=headers,data=json.dumps(data))
            response_json =response.json()
            if response_json and response_json["status"]== True:
                checkoutpage = response_json["data"]["authorization_url"]
                return redirect(checkoutpage)
            else:
                flash(f"Paystack returned an error {response_json['message']}", category='error')
                return redirect("/home/cart/")
        except:
            flash('we could not connect to paystack try again later', category='error')
            return redirect("/home/cart/")
    else:
        flash("please complete the form", category='error')
        return redirect("/home/cart/")






@userobj.route("/pay/landing/")
def payment_landing_page():
    id = session.get('useronline')
    userdets = get_user_by_id(id)
    ref = session.get("payref")
    paystackref= request.args.get("reference") 
    if ref == paystackref:
        url="https://api.paystack.co/transaction/verify/"+ref
        headers= {"Content-Type":"application/json",
                  "Authorization": "Bearer sk_test_22401be45dc31477f629d7ab5b95924fe9318d4f"
                  }
        response = requests.get(url,headers=headers)
        response_json =response.json()
        # return response_json
        tran = Transaction.query.filter(Transaction.serial_number==ref).first()
        order= Orders.query.filter(Orders.buyer_id==id)
        if response_json["status"]== True:
            ip = response_json['data']["ip_address"]
            order.status="confirmed"
            tran.transaction_status = "completed"
            tran.transaction_date = datetime.now()
            order.ip_address=ip
        else:
            order.status="failed"
            tran.transaction_status = "failed"
        session.pop('Shoppingcart')
        db.session.commit()
        return redirect('/home/homepage/')
           
    else:
        flash("invalid parameter detected", category='error')
        return redirect("/reports/")







@userobj.route('/confirmpayment/', methods=['GET', 'POST'])
@login_required
def confirmpayment():
    id = session.get('useronline')
    userdets = get_user_by_id(id)
    total = session.get('grandtotal')
    proquantity = request.form.get('quantity')
    ref = "WISE" + secrets.token_hex(5)
    
    order = Orders(buyer_id=id, total_amount=total, status='pending')
    db.session.add(order)
    db.session.commit()
    
    order_id = order.order_id
    
    for key, product in session['Shoppingcart'].items():
        print(proquantity)
        orderitem = Order_items(order_id=order_id, product_id=key,buyer_id=id)
        payment = Transaction(buyer_id=id, amount=total, serial_number=ref,transaction_status="pending")
        db.session.add_all([orderitem, payment])
    
    db.session.commit()
    
    session['payref'] = ref
    
    return render_template('user/payconfirm.html', userdets=userdets, total=total)
        # return redirect("/home/homepage/")





@userobj.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session["Shoppingcart"]) <= 0:
        return redirect('/home/homepage/')
    try:
        session.modified= True
        for key, item in session['Shoppingcart'].items():
            if int(key)== id:
                session['Shoppingcart'].pop(key, None)
                return redirect('/home/cart/')
    except Exception as e:
        print(e)
        return redirect('/home/cart/')




@userobj.route('/address/', methods=['Get','POST'])
@login_required
def address():
    phone1 = request.form.get('phone1')
    address = request.form.get('inputaddress')
    city= request.form.get('inputcity')
    state = request.form.get('inputstate')
    zip= request.form.get('inputzip')
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    if address:
        user = User.query.get(id) 
        user.address=address
        user.city=city
        user.phone_number=phone1
        user.state=state
        user.zip=zip
        db.session.commit()
        flash("adress saved successfully",category="success")
        return render_template('user/settings.html', userdets=userdets)
    else:
        return render_template('user/address.html', userdets=userdets)




@userobj.route('/admin/')
def admin():
    id= session.get('useronline')
    if id != None:
        userdets= get_user_by_id(id)
        return render_template('user/admin.html', userdets=userdets)

    else:
        flash("you must be logged in to view this page", category="error")
        return redirect('/home/login/')

@userobj.route('/management/')
@login_required

def management():
    id= session.get('useronline')
    if id != None:
        userdets= get_user_by_id(id)
        return render_template('user/management.html', userdets=userdets)

    else:
        flash("you must be logged in to view this page", category="error")
        return redirect('/home/login/')


@userobj.route('/notification/')
def notification():
    id= session.get('useronline')
    if id != None:
        userdets= get_user_by_id(id)
        return render_template('user/notification.html', userdets=userdets)

    else:
        flash("you must be logged in to view this page", category="error")
        return redirect('/home/login/')



@userobj.route('/settingssmall/')

def settingssmall():
    id= session.get('useronline')
    if id != None:
        userdets= get_user_by_id(id)
        return render_template('user/settingssmall.html', userdets=userdets)

    else:
        flash("you must be logged in to view this page", category="error")
        return redirect('/home/login/')
    





@userobj.route('/close/', methods=['GET','POST'])
def close():
    id= session.get('useronline')
    if id != None:
        posts = db.session.query(User).get_or_404(id)
        db.session.delete(posts)
        db.session.commit()
        return render_template('user/login.html')
    else:
        flash("you must be logged in to view this page", category="error")
        return redirect('/home/login/')


@userobj.route('/subscribe/')
def subscription():
    id= session.get('useronline')
    if id != None:
        userdets= get_user_by_id(id)
        return render_template('user/subscription.html',userdets=userdets)

    else:
        flash("you must be logged in to view this page", category="error")
        return redirect('/home/login/')





@userobj.route('/header/',methods=['GET'])
def header():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    catig = Category.query.all()
    return render_template('user/headerlogged.html',catig=catig,userdets=userdets)



@userobj.route('/head/',methods=['GET'])
def head():
    id= session.get('useronline')
    userdets= get_user_by_id(id)
    catig = Category.query.all()
    return render_template('user/header.html',catig=catig,userdets=userdets)





@userobj.route('/logout/')
def logout():
    if session.get("useronline"):
        session.pop('useronline')
    elif session.get('Shoppingcart'):
        session.pop('Shoppingcart')
    return redirect('/home/login/')
    


    
@errorbp.app_errorhandler(404)
@login_required
def page_not_found(error):
    id= session.get('useronline')
    if id != None:
        userdets= get_user_by_id(id)
    return render_template('user/pagenotfounderror.html',userdets=userdets),404
































@userobj.after_request
def fun_after_request(response):

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response



@userobj.route('/empty/')
def empty():
    session.clear()
    return redirect("/home/homepage/")