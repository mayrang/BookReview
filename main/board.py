from main import redirect, url_for, request, mongo
from flask import Blueprint

bp = Blueprint("board", __name__, url_prefix="/board")

bp.route("/review_list")
def review_list():
    review = mongo.db.review
    return ""