import os
from dotenv import load_dotenv
import pyrebase

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

#app.secret_key = os.getenv('SECRET_KEY')
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def insert(val1, val2, val3, val4, val5, val6):
    data = {
        "answer1" : val1, 
        "answer2" : val2, 
        "answer3" : val3, 
        "answer" : val4, 
        "category_id" : val5, 
        "title" : val6
        }
    db.child("questions").push(data)

def categ(val1, val2):
    data = {
        "id" : val1, 
        "name" : val2 
    }
    db.child("categories").push(data)

  
all_users = db.child("categories").get()
for user in all_users.each():
    print(user.key()) # Morty
    print(user.val()['name']) # {name": "Mortimer 'Morty' Smith"}