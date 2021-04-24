from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wad

app = Flask(__name__)


@app.route("/")
def index():
    users = db.users.find({})
    return render_template("index.html")

@app.route('/cabinet', methods=['POST'])
def login():
    password = request.form['pass']
    login_user = db.users.find_one({'name' : request.form['username']})

    if login_user and password:
        if request.form['pass']  == login_user['password']:
            return render_template('image.html')
    else:
          return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = db.users.find_one({'name' : request.form['username']})

        if existing_user is None:
            db.users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

