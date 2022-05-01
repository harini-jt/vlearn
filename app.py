import bcrypt
import pymongo
from flask import Flask, render_template, request, url_for, redirect, session
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

# set app as a Flask instance
app = Flask(__name__)
# encryption relies on secret keys so they could be run
app.secret_key = os.environ.get('SECRET_KEY')

# connect to your Mongo DB database
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))

# get the database name
db = client.get_database('DB_NAME')
users = db[os.environ.get('USERS_COLLECTION')]


@app.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    # if method post in index
    if "email" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form.get('role')
        isOnline = True
        # if found in database showcase that it's found
        user_found = users.find_one({"name": user})
        email_found = users.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email,
                          'password': hashed, 'role': role, "isOnline": isOnline}
            # insert it in the record collection
            users.insert_one(user_input)

            # find the new created account and its email
            user_data = users.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            return render_template('profile.html', email=new_email)
    return render_template('signup.html')


@app.route('/home', methods=['GET'])
def home():
    # base -> only nav bar
    return render_template('base.html')


if __name__ == "__main__":
    app.secret_key = os.environ.get('SECERT_KEY')
    app.run('127.0.0.1', 5000, debug=True)
