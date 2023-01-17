from flask import Flask,render_template,request,url_for,flash
from flask import Flask,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_manager,login_user,logout_user,LoginManager
from flask_login import login_required,current_user


#connecting the db
local_server = True
app = Flask(__name__)
app.secret_key='ss'

login_manager=LoginManager(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/ecms'
db=SQLAlchemy(app)

#creating db tables

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)

class Cart(db.Model):
   order_id=db.Column(db.Integer,primary_key=True)
   email=db.Column(db.String(20))
   name=db.Column(db.String(20))
   address=db.Column(db.String(50))
   pincode=db.Column(db.Integer) 
   number=db.Column(db.String(12))
   product=db.Column(db.String(20))


    #with app.app_context():
    #db.create_all()
   
     


 
@app.route('/')
def hello_world():
   return render_template('index.html')
   
@app.route('/products')
@login_required
def products():
   
    
   return render_template('products.html')


@app.route('/cart',methods=['POST','GET'])
@login_required
def cart():
   if request.method=="POST":
      email=request.form.get('email')
      name=request.form.get('name')
      product=request.form.get('product')
      address=request.form.get('address')
      pincode=request.form.get('pincode')
      number=request.form.get('number')

      query=db.engine.execute(f"INSERT INTO `cart` (`email`,`name`,`product`,`address`,`pincode`,`number`) VALUES('{email}','{name}','{product}','{address}','{pincode}','{number}')")
      

   return render_template('cart.html')

@app.route('/order_details')
@login_required
def order_details():
   em=current_user.email
   query=db.engine.execute(f"SELECT * FROM `cart` WHERE email='{em}'")
   return render_template('order_details.html',query=query)

@app.route('/edit/<string:order_id>',methods=['POST','GET'])
@login_required
def edit(order_id):
   posts = Cart.query.filter_by(order_id=order_id).first()

   if request.method=="POST":
      email=request.form.get('email')
      name=request.form.get('name')
      product=request.form.get('product')
      address=request.form.get('address')
      pincode=request.form.get('pincode')
      number=request.form.get('number')
      db.engine.execute(f"UPDATE `cart` SET  `email` = '{email}', `name` = '{name}', `address` = '{address}', `pincode` = '{pincode}', `number` = '{number}', `product` = '{product}' WHERE `cart`.`order_id` = {order_id}")
      return redirect('/order_details')
   return render_template('edit.html',posts=posts)


@app.route('/delete/<string:order_id>',methods=['POST','GET'])
@login_required
def delete(order_id):
   db.engine.execute(f"DELETE FROM `cart` WHERE `cart`.`order_id`={order_id}")
   return redirect('/order_details')

@app.route('/listed')
@login_required
def listed():
   return render_template('listed.html')

@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')
   
@app.route('/signup',methods=['GET','POST'])
def signup():

   if request.method == "POST":
      username=request.form.get('username')
      email=request.form.get('email')
      password=request.form.get('password')
      encpass=generate_password_hash(password)
      user=User.query.filter_by(email=email).first()
      if user:
         print('email exists')
         return render_template('/signup.html')
       
      #encpass=generate_password_hash(passw)
      new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpass}')")
      #newuser=User(user=username,email=email,password=password)
      #db.session.add(newuser)
      #db.session.commit()


      return render_template ('login.html')
   
   return render_template ('signup.html')
 



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
    
      email=request.form.get('email')
      password=request.form.get('password')
      user=User.query.filter_by(email=email).first()

      if user and check_password_hash(user.password,password):
         login_user(user)
         #flash("Logged In","primary")
         return redirect (url_for('products'))
      else :
         #flash("invalid credentials","danger")
         return render_template ('login.html')



    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
   
   
   


app.run(debug=True)


#username=current_user.username