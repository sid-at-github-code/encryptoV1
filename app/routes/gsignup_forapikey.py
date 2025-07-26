from ..utilities import generate_api_token
from urllib.parse import urlencode
from flask import Blueprint, jsonify,request,redirect
from dotenv import load_dotenv
import redis 
import os
get_token_bp = Blueprint("get_token_bp", __name__)

try:
    load_dotenv()
    my_redis_url = os.environ.get("REDIS_URL")
    if not my_redis_url:
        raise ValueError("Unable to fetch or access the Redis URL from .env")
except Exception as e:
    raise Exception({"error in env redis_url loading": f"Unexpected error: {str(e)}"})
    
r = redis.Redis.from_url(my_redis_url)

@get_token_bp.route("/get-token",methods=["POST"])
def getting():
    email= request.json.get("email")

    # Generate token
    token = generate_api_token(email)

    # ⏳ Get token expiry from Redis
    expiry = r.ttl(token)
    if expiry == -2:
        expiry_message = "API key has expired"
    elif expiry == -1:
        expiry_message = "API key exists and has no expiration"
    else:
        days = expiry // 86400
        hours = (expiry % 86400) // 3600
        expiry_message = f"{days} days, {hours} hours remaining"

    # 📦 Send back to frontend as query string
    query = urlencode({
        "token": token,
        "email": email,
        "expiry": expiry_message,
        "signedIn": True
    })
    frontend_url = os.getenv("FRONTEND_URL")
    pack={"link":f"{frontend_url}/api-access?{query}"}
    return jsonify(pack)  
    # 🔁 Redirect to frontend
    
    
#use it to  get expiry of the key 
@get_token_bp.route("/get-api-expiry", methods=["POST"])
def get_api_expiry():
    data=request.get_json()
    key=data.get("api_key")
    if not key:
        return jsonify({"error": "API key not found"}), 404
    expiry = r.ttl(key)
    days = expiry // 86400
    remaining_seconds = expiry % 86400
    hours = remaining_seconds // 3600
    val=f"{days} days, {hours} hours remaining"
    if expiry == -2:
        return jsonify({"show": "API key has expired"}), 404
    elif expiry == -1:
        return jsonify({"show": "API key exists and has no expiration"}), 200
    else:
        return jsonify({"show": val}), 200
    
    
    
    