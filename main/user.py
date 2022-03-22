from flask import Blueprint, session
from main import *

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/join", methods=["POST", "GET"])
def join():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if name == "" or email == "" or password1 == "" or password2 == "":
            flash("입력하지 않은 항목이 있습니다")
            return redirect(url_for('user.join'))
        user = mongo.db.user
        email_cnt = user.count_documents({"email" : email})
        if email_cnt > 0:
            flash("이메일이 중복됐습니다.")
            return redirect(url_for('userjoin'))
        if password1 != password2:
            flash("비밀번호 확인을 다시해주세요")
            return redirect(url_for('user.join'))
        password = make_hash_password(password1)
        post = {
            "name": name,
            "email": email,
            "password": password,
            "login_count": 0,
            "login_time": None
        }
        idx = user.insert_one(post)
        session["id"] = str(idx)
        session["email"] = email
        session["name"] = name
        return redirect(url_for('home.home'))
    else:
        return render_template("user_join.html")
        
        
@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == "" or password == "":
            flash("입력하지 않은 항목이 있습니다.")
            return redirect(url_for('user.login'))
        user = mongo.db.user
        email_check = user.count_documents({"email" : email})
        if email_check == 0:
            flash("이메일이 올바르지 않습니다.")
            return redirect(url_for('user.login'))
        user_one = user.find_one({"email" : email})
        if not check_password(user_one.get("password"), password):
            flash("비밀번호가 올바르지 않습니다.")
            return redirect(url_for('user.login'))
        session["id"] = str(user_one.get("_id"))
        session["name"] = str(user_one.get("name"))
        session["email"] = str(user_one.get("email"))
        session.permanent = True
        return redirect(url_for('board.review_list'))
    else:
        return render_template("user_login.html")

