from flask import Flask, redirect, request, jsonify, render_template
import numpy as np
import pickle
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

model = pickle.load(open('model.pkl','rb'))

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    def __init__(self,username,password):
        self.username = username
        self.password = password

with app.app_context():
    db.create_all()
    db.session.commit()


isLoggedIn = False

@app.route('/predict', methods=['GET','POST'])
def predict():
    if not isLoggedIn:
        return redirect('/')
    elif isLoggedIn and request.method == 'GET' :
        return render_template('predict.html')
    elif (isLoggedIn and request.method == 'POST'):
        return render_template('predict.html', message=f"You are eligible for loan")



@app.route('/login', methods=['GET','POST'])
def login():
    global isLoggedIn
    if isLoggedIn == False and request.method == 'GET' :
        return render_template('login.html')
    elif isLoggedIn == False and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = UserInfo.query.filter_by(username=username).first()
            if user.username == username and user.password == password:
                isLoggedIn = True
                return redirect('/predict')
            elif user.username == username and user.password != password:
                return render_template('login.html', message="Password is do not match")
        except Exception as e:
            return render_template('login.html', message="Username not registered/invalid")
          
    elif isLoggedIn == True:
        return redirect('/predict')



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method == 'POST':
        ## collect username & password from the form
        username = request.form['username']
        password = request.form['password']
        try:
            new_user = UserInfo(username,password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('register.html', message="User created successfully")
        except Exception as e:
            return render_template('register.html', message=f"Username already exists")



@app.route('/logout')
def logout():
    global isLoggedIn 
    isLoggedIn = False
    return render_template('logout.html')



@app.route('/')
def home():
    return render_template('home.html')
 
    

if __name__ == '__main__':
    app.run(debug=True)