
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

def rate_limit(limit: int, window: int):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                client_ip = request.remote_addr or "unknown"
                route_key = f"rate:{client_ip}:{request.endpoint}"

                current = r.incr(route_key)
                if current == 1:
                    r.expire(route_key, window)

                if current > limit:
                    return jsonify({"error": "Too many requests"}), 429

                return fn(*args, **kwargs)
            except redis.RedisError:
                # Optional: fail open (don't block if Redis goes down)
                return fn(*args, **kwargs)
        return wrapper
    return decorator
