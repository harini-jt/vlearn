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


@app.route('/', methods=['GET'])
def home():
    # base -> only nav bar
    return render_template('base.html')




@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists in database
        email_found = users.find_one({"email": email})

        # STUDENT
        if email_found and email_found['role'] == os.environ.get('STUDENT'):
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                db.users.find_one_and_update({'email': session['email']}, {
                                             '$set': {'isOnline': True}})
                return redirect(url_for('profile'))
            else:
                if "email" in session:
                    db.users.find_one_and_update({'email': session['email']}, {
                                                 '$set': {'isOnline': True}})
                    return redirect(url_for("profile"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        # TEACHER
        elif email_found and email_found['role'] == os.environ.get('TEACHER'):
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                db.users.find_one_and_update({'email': session['email']}, {
                                             '$set': {'isOnline': True}})
                return redirect(url_for("profile"))

            else:
                if "email" in session:
                    db.users.find_one_and_update({'email': session['email']}, {
                        '$set': {'isOnline': True}})
                    return redirect(url_for("profile"))

                message = 'Wrong password'
                return render_template('login.html', message=message)
        # ADMIN
        elif email_found and email_found['role'] == os.environ.get('ADMIN'):
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                db.users.find_one_and_update({'email': session['email']}, {
                                             '$set': {'isOnline': True}})
                return redirect(url_for("admin"))

            else:
                if "email" in session:
                    db.users.find_one_and_update({'email': session['email']}, {
                        '$set': {'isOnline': True}})
                    return redirect(url_for("admin"))
                message = 'Wrong password'
                return render_template('login.html', message=message)

        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)
