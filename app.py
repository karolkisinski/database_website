from flask import Flask, render_template, session, request, redirect, flash
import os
from dotenv import load_dotenv
import pyrebase
from auth import insert, ca, qu, get_questions_by_category
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
        return render_template('categories.html', categories=ca())
    else:
         flash(f"Logowanie wymagane!", "error")
         return render_template('login.html')

@app.route('/add_question', methods=['POST', 'GET'])
def add_question():
    if('user' in session):
        if request.method == 'POST':
            title = request.form.get('title')
            validanswer = request.form.get('validanswer')
            badanswer1 = request.form.get('badanswer1')
            badanswer2 = request.form.get('badanswer2')
            badanswer3 = request.form.get('badanswer3')
            category = request.form.get('category')
            try:
                string = "{}, " ", {}, " ", {}, " ", {}, " ", {}, " ", {}".format(title, validanswer, badanswer1, badanswer2, badanswer3, category)
                insert(badanswer1, badanswer2, badanswer3, validanswer, category, title)
                flash("Pytanie dodane!")
                return render_template('add_question.html', categories=ca())
            except:
                flash(f"Cos poszlo nie tak :(", "error")
                return render_template('add_question.html', categories=ca())
        return render_template('add_question.html', categories=ca())
    else:
         flash(f"Logowanie wymagane!3", "error")
         return render_template('login.html')

@app.route('/questions')
def get_questions():
     if('user' in session):
        try:
            questions = qu()
            return render_template('show_questions.html', questions = questions)
        except:
            flash(f"Cos poszlo nie tak :(", "error")

@app.route('/questions/<id>')
def questions_by_category(id):
     if('user' in session):
        try:
            questions = get_questions_by_category(id)
            return render_template('show_questions.html', questions = questions)
        except:
            flash(f"Cos poszlo nie tak :(", "error")
            return render_template('home.html')

def parseCSV(file):
    print("hellol")
    import pandas as pd
    col_names = ['answer1','answer2','answer3', 'validAnswer', 'title' , 'categoryId']
    csvData = pd.read_csv(file,names=col_names, header=None)
    for i,row in csvData.iterrows():
        insert(row['answer1'], row['answer2'], row['answer3'], row['categoryId'], row['title'], row['validAnswer'])

@app.route('/import', methods=['GET','POST'])
def import_questions_from_file():
    if(request.method!="POST"):
        return render_template('import.html')
    if(request.method=="POST"):
        try:
            uploaded_file = request.files['file']
            print(uploaded_file)
            if uploaded_file.filename != '':   
                print("A TUTAJ?")
                file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), uploaded_file.filename)
                uploaded_file.save(file_path)
                parseCSV(file_path)
                flash(f"Pytania zostały wczytane!", "success")
                return render_template("import.html")
            else:
                flash(f"Plik nie został wczytany!", "error")
                return render_template("import.html")
        except:
            flash(f"Cos poszlo nie tak :(", "error")
            return render_template("import.html")

if __name__ == '__main__':
    app.run(debug=True)

