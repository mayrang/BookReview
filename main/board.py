from pydoc import render_doc
from main import redirect, url_for, request, mongo
from flask import Blueprint, render_template
import math

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
                                                block_start=block_start,
                                                block_end=block_end)
    
    
        
                        