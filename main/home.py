from flask import Blueprint
from main import redirect, url_for


bp = Blueprint("home", __name__)
@bp.route("/")
def home():
    return redirect(url_for('board.review_list'))