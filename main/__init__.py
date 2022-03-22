from email.utils import format_datetime
from flask import Flask
from flask_pymongo import PyMongo
from flask import redirect, url_for, request, render_template, flash
from datetime import timedelta
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/BookReview"
app.config["SECRET_KEY"] = "elkajtlkajdlknatylk"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

ALLOWED_EXTENTIONS = set(["png", "jpeg", "jpg"])
BOARD_IMAGE_PATH = "C:\\bookreview\\images"

app.config["ALLOWED_EXTENTIONS"] = ALLOWED_EXTENTIONS
app.config["BOARD_IMAGE_PATH"] = BOARD_IMAGE_PATH
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])


mongo = PyMongo(app)


from .filter import format_datetime
from .common import check_password, make_hash_password
from . import board, home, user


app.register_blueprint(board.bp)
app.register_blueprint(home.bp)
app.register_blueprint(user.bp)