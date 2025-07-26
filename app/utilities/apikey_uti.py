import secrets
from dotenv import load_dotenv
import redis  
import os
from functools import wraps
from flask import jsonify, request
try:
    load_dotenv()
    my_redis_url = os.environ.get("REDIS_URL")
    if not my_redis_url:
        raise ValueError("Unable to fetch or access the Redis URL from .env")
except Exception as e:
    raise Exception({"error in env redis_url loading": f"Unexpected error: {str(e)}"})
    
r = redis.Redis.from_url(my_redis_url)

def generate_api_token(email: str) -> str:
    if r.hexists("api_bank", email):
        val = r.hget("api_bank",email)
        val=val.decode()
        return val
    else:
        token = secrets.token_hex(16)
        token=f"encrypto-key:{token}"
        r.set(token, email, ex=864000)#10 days
        r.hset("api_bank",email,token)
        return token

def validate_token(token: str) -> bool:
    tf=bool(r.exists(token))
    return tf and token.startswith("encrypto-key:")

def get_email_from_token(token: str) -> str:
    email=r.get(token)
    email=email.decode()
    return email

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-api-key")
        if not token or not validate_token(token):
            return jsonify({"error": "Unauthorized"}), 401
        
        request.user_email = get_email_from_token(token)  # you can access this in the view
        return func(*args, **kwargs)
    return wrapper
#test
if __name__=="__main__":
    x=generate_api_token("sid@gmail.com")
    print(x)
    