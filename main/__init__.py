from flask import Flask
from flask_pymongo import PyMongo
from flask import redirect, url_for, request, render_template

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/BookReview"
app.config["SECRET_KEY"] = "elkajtlkajdlknatylk"


mongo = PyMongo(app)

