from email.utils import format_datetime
from flask import Flask
from flask_pymongo import PyMongo
from flask import redirect, url_for, request, render_template, flash
from datetime import timedelta

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/BookReview"
app.config["SECRET_KEY"] = "elkajtlkajdlknatylk"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

mongo = PyMongo(app)


from .filter import format_datetime
from .common import check_password, make_hash_password
from . import board, home, user


app.register_blueprint(board.bp)
app.register_blueprint(home.bp)
app.register_blueprint(user.bp)