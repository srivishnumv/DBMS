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


 
@app.route("/")
def hello_world():
   return render_template('index.html')
   

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/home')
def home():
    return 'this is my home'


app.run(debug=True)
