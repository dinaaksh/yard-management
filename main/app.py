from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api
from api import UserAPI,TruckAPI  
import requests as rq
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'palampur_ftw'

def getdb():
    conn = sqlite3.connect('warehouse.db')
    return conn

api = Api(app)
api.add_resource(UserAPI, '/api/user')
api.add_resource(TruckAPI, '/api/truck')

# Redirect root URL to login page
@app.route('/')
def home():
    return redirect(url_for('login'))

# REGISTRATION LOGIC
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        employeeid = request.form['employeeid']
        password = request.form['password']
        role = request.form['role']

        # Call the UserAPI to register the user
        response = rq.post('http://localhost:5000/api/user', json={
            'employeeid': employeeid,
            'password': password,
            'name': name,
            'role': role
        })

        if response.status_code == 400:
            error = response.json().get('message', 'An error occurred.')
            return render_template('register.html', error=error)
        elif response.status_code == 200:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="An unexpected error occurred.")

    return render_template('register.html')

# LOGIN LOGIC
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = {
            'employeeid': request.form['employeeid'],
            'password': request.form['password']
        }
        try:
            response = rq.get(request.url_root + 'api/user', json=login)
            
            # Check if the response is empty
            if response.text.strip() == '':
                return render_template('login.html', err="No response from the server.")
            
            # Try to parse JSON response
            role_json = response.json()
            message = role_json.get('message')
            role = role_json.get('role')
            
            if message == 'Login Successful':
                if role == 'Master Controller':
                    return redirect(url_for('masterdash'))
                else:
                    return redirect(url_for('userdash'))
            else:
                return render_template('login.html', err=message)
                
        except rq.exceptions.JSONDecodeError:
            return render_template('login.html', err="Invalid response format from the server.")
        except Exception as e:
            # Log the exception and show a general error message
            print(f"An error occurred: {e}")
            return render_template('login.html', err="An error occurred during login.")

    return render_template('login.html')

@app.route('/masterdash')
def masterdash():
    conn=getdb()
    truck=conn.execute("SELECT * FROM trucks").fetchall()
    skus=conn.execute("SELECT * FROM skus").fetchall()
    stores=conn.execute("SELECT * FROM stores").fetchall()
    return render_template('masterdash.html', truckdata=truck, skus=skus, stores=stores)

@app.route('/userdash')
def userdash():
    return render_template('userdash.html')

if __name__ == '__main__':
    app.run(debug=True)

