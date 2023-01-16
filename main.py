from flask import Flask,render_template,request,url_for
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

    #with app.app_context():
    #db.create_all()
   
     


 
@app.route('/')
def hello_world():
   return render_template('index.html')
   
@app.route('/products')
def products():
   if not User.is_authenticated:
      return render_template('login.html')
   else :
      #username=current_user.username
      return render_template('products.html',username=current_user.username)
   return render_template('products.html')


@app.route('/cart')
def cart():
   return render_template('cart.html')

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
         return redirect (url_for('products'))
      else :
         print('invalid credentials')

         return render_template ('login.html')



    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
   
   
   


app.run(debug=True)


#username=current_user.username