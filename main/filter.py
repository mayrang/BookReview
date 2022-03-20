from main import *
import time
from datetime import datetime

@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None and value == "":
        return ""
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp(int(value/1000)) + offset
    return value.strftime("%Y-%m-%d %H:%M:%S")