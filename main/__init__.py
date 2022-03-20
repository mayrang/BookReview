from email.utils import format_datetime
from flask import Flask
from flask_pymongo import PyMongo
from flask import redirect, url_for, request, render_template

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/BookReview"
app.config["SECRET_KEY"] = "elkajtlkajdlknatylk"


mongo = PyMongo(app)

from . import board, home
from .filter import format_datetime

app.register_blueprint(board.bp)
app.register_blueprint(home.bp)