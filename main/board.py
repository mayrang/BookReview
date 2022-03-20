from pydoc import render_doc
from main import redirect, url_for, request, mongo
from flask import Blueprint, render_template, abort
from flask_pymongo import ObjectId
import math
from datetime import datetime


bp = Blueprint("board", __name__, url_prefix="/board")

@bp.route("/review_list")
def review_list():
    page = request.args.get("page", 1, int)
    review = mongo.db.review
    search = request.args.get("search", 0, int)
    search_value = request.args.get("searchValue", "", str)
    sort_method = request.args.get("sortMethod", "time", str)
    search_list = []
    limit = 10
    query = {}
    if search == 1:
        search_list.append({"title": {"$regex": search_value}})
    elif search == 2:
        search_list.append({"title": {"$regex": search_value}})
        search_list.append({"contents": {"$regex": search_value}})
    elif search == 3:
        search_list.append({"user_name": {"$regex": search_value}})
        
    if len(search_list) > 0:
        query = {"$or": search_list}
    
    if sort_method == "time":
        review_list = review.find(query).sort("pubdated", -1).skip(limit*(page-1)).limit(limit)
    elif sort_method == "recommend":
        review_list = review.find(query).sort({"recommend_count": -1}).skip(limit*(page-1)).limit(limit)
    
    total_count = review.count_documents(query)
    last_page_num = int(math.ceil(total_count/limit))
    block_size = 10
    page_block = int((page-1)/block_size)
    block_start = page_block * block_size + 1
    block_end = page_block * block_size + block_size
    return render_template("review_list.html", review_list=review_list,
                                                search=search,
                                                search_value=search_value,
                                                sort_method=sort_method,
                                                last_page_num=last_page_num,
                                                page_block=page_block,
                                                page=page,
                                                limit=limit,
                                                block_start=block_start,
                                                block_end=block_end)
    
    
@bp.route("/write_review", methods=["POST", "GET"])
def write_review():
    if request.method == "GET":
        return render_template("write_review.html")
    else:
        name = request.form.get("user_name")
        title = request.form.get("title")
        content = request.form.get("content")
        pub_time = round(datetime.utcnow().timestamp() * 1000)
        view_count = 0
        recommend_count = 0
        review = mongo.db.review
        post = {
            "name": name,
            "title": title,
            "content": content,
            "pub_time": pub_time,
            "view_count": view_count,
            "recommend_count": recommend_count
        }
        idx = review.insert_one(post)
        return redirect(url_for('board.review_list'))
        
        
@bp.route("/review_view/<idx>")
def review_view(idx):
    sort_method = request.args.get("sortMethod")
    search = request.args.get("search")
    search_value = request.args.get("searchValue")
    review = mongo.db.review
    view = review.find_one_and_update({"_id": ObjectId(idx)},
                                      {"$inc": {"view_count": 1}},
                                      return_document=True)
    if view is not None:
        review = {
            "name": view.get("name"),
            "title": view.get("title"),
            "content": view.get("content"),
            "pub_time": view.get("pub_time"),
            "view_count": view.get('view_count')
        }
        return render_template("review_view.html", review=review,
                                                search=search,
                                                search_value=search_value,
                                                sort_method=sort_method)  
    return abort(404) 