from flask import Flask, render_template, session, request, redirect
import os
from dotenv import load_dotenv
import pyrebase
from auth import insert
app = Flask(__name__)

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
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return "You were logged in successfully"
        except:
            return 'Failed to login'
    return render_template('home.html')

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

if __name__ == '__main__':
    app.run(debug=True)
