"""src/page_tracker/app.py
the source code for the lil flask app
used by the RealPython docker CI tutorial."""

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """defines behavior when you go to the main page"""
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")  # log the problem via Flask
        return "Sorry, something went wrong \N{PENSIVE FACE}", 500
        # returns second arg (error status code)
    else:
        return f"This page has been seen {page_views} times."


#  put client creation into a function so it is not global scope
#    (for mocking purposes)
@cache  # cached to ensure only one instance of it in memory
def redis():
    """get Redis client"""
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
