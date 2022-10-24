from flask import Flask, render_template, session, request, redirect, flash
import os
from dotenv import load_dotenv
import pyrebase
from auth import insert
app = Flask(__name__,
            static_folder='templates/static')

load_dotenv()

config = {
  'apiKey': os.getenv('apiKey'),
  'authDomain': os.getenv('authDomain'),
  'databaseURL': os.getenv('databaseURL'),
  'projectId': os.getenv('projectId'),
  'storageBucket': os.getenv('storageBucket'),
  'messagingSenderId': os.getenv('messagingSenderId'),
  'appId': os.getenv('appId')
}

app.secret_key = os.getenv('SECRET_KEY')
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/', methods=['POST', 'GET'])
def home():
    if('user' in session):
        return render_template('home.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            flash(f"Zalogowano pomyślnie!", "success")
            return render_template('home.html')
        except:
            flash(f"Logowanie nieudane!", "error")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/categories')
def categories():
    if('user' in session):
        return render_template('categories.html')
    else:
         flash(f"Logowanie wymagane!", "error")
         return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

