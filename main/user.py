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
        