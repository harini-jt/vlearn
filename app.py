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

@app.route('/', methods=['GET'])
def home():
    # base -> only nav bar
    return render_template('base.html', message =  os.environ.get('SECRET_KEY'))

