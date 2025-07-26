
# testing truf for redis 



import redis
import os 
from dotenv import load_dotenv

from functools import wraps
from flask import request, jsonify
import redis

# Connect to Redis
try:
    load_dotenv()
    my_redis_url = os.environ.get("REDIS_URL")
    if not my_redis_url:
        raise ValueError("Unable to fetch or access the Redis URL from .env")
except Exception as e:
    print({"error in env redis_url loading": f"Unexpected error: {str(e)}"})

r = redis.Redis.from_url(my_redis_url)

r.flushall()