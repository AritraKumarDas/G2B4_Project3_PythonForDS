from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl','rb'))


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/')
def home():
    return render_template('home.html')
    
    # if request.method == 'GET':
    #     return render_template('index.html')
    
    # age_of_car = int(request.form['Age_of_the_car'])
    # present_price = float(request.form['Present_Price'])
    # kms_driven = float(request.form['Kms_Driven'])
    # owner = int(request.form['Owner'])
    # fuel_type = int(request.form['Fuel_Type'])
    # seller_type = int(request.form['Seller_Type'])
    # transmission = int(request.form['Transmission'])

    # prediction = model.predict([[present_price,kms_driven,fuel_type, seller_type, transmission, owner, age_of_car ]])
    # output = round(prediction[0],2)
    # return render_template('index.html',prediction_text = f"Predicted Selling Price : {output} Lakhs" ) 
    

if __name__ == '__main__':
    app.run(debug=True)