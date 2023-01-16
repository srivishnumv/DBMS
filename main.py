from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

#connecting the db
local_server = True
app = Flask(__name__)
app.secret_key='ss'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/ecms'
db=SQLAlchemy(app)

#creating db tables

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))


 
@app.route('/')
def hello_world():
   return render_template('index.html')
   
@app.route('/products')
def products():
   return render_template('products.html')

@app.route('/cart')
def cart():
   return render_template('cart.html')

@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')
   
@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/logout')
def logout():
   return render_template('login.html')
   
   
   


app.run(debug=True)
