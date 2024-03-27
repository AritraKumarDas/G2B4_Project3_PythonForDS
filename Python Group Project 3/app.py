from flask import Flask, redirect, request, jsonify, render_template, session
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


app.secret_key = 'aritra_session_key'


@app.route('/predict', methods=['GET','POST'])
def predict():
    if ('isLoggedIn' not in session) or (session['isLoggedIn'] == False):
        return redirect('/')
    elif session['isLoggedIn']==True and request.method == 'GET' :
        return render_template('predict.html', username=session['username'])
    elif (session['isLoggedIn']==True and request.method == 'POST'):
        gender = int(request.form['gender'])
        married = int(request.form['married'])
        dependents = int(request.form['dependents'])
        education = int(request.form['education'])
        self_employed = int(request.form['self-employed'])
        applicant_income = float(request.form['applicant-income'])
        co_applicant_income = float(request.form['co-applicant-income'])
        loan_amount = float(request.form['loan-amount'])
        loan_term = int(request.form['loan-term'])
        credit_history = float(request.form['credit-history'])
        property_area = int(request.form['property-area'])

        prediction =  model.predict([[gender,married, dependents, education, self_employed, applicant_income,co_applicant_income, loan_amount, loan_term,credit_history,property_area]])

        output_msg = f"Congratulations! {session['username']}, you are eligible for loan!" if (prediction[0] == 'y' or prediction[0] == 'Y') else f"Sorry! {session['username']}, you are not eligible for loan"

        return render_template('predict.html', message=output_msg, username=session['username'])



@app.route('/login', methods=['GET','POST'])
def login():
    
    if ( ('isLoggedIn' not in session) or (session['isLoggedIn'] == False) ) and request.method == 'GET' :
        return render_template('login.html')
    elif ( ('isLoggedIn' not in session) or (session['isLoggedIn'] == False) ) and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = UserInfo.query.filter_by(username=username).first()
            if user.username == username and user.password == password:
                session['isLoggedIn'] = True
                session['username'] = username
                return redirect('/predict')
            elif user.username == username and user.password != password:
                return render_template('login.html', message="Password do not match")
        except Exception as e:
            return render_template('login.html', message="Username not registered/invalid")
          
    elif 'isLoggedIn' in session and session['isLoggedIn'] == True:
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
    session['isLoggedIn'] = False
    session.pop('username',default=None)
    return render_template('logout.html')



@app.route('/')
def home():
    return render_template('home.html')
 

if __name__ == '__main__':
    app.run(debug=True)
