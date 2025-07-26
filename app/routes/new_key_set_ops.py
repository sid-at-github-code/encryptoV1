import redis
import os 
from dotenv import load_dotenv 

from ..logics import shuffler
from ..logics import encoder
from ..logics import finalandsigner

from ..utilities import HazardProcessor
from ..utilities import require_api_key
from ..utilities import rate_limit
from functools import wraps

from flask import Blueprint, jsonify,request

kv_bp = Blueprint("kv_bp", __name__)

# stable connection establishment 
load_dotenv()

try:
    my_redis_url = os.environ.get("REDIS_URL")
    if not my_redis_url:
        raise ValueError("Unable to fetch or access the Redis URL from environment variables.")

    r = redis.Redis.from_url(my_redis_url)    

except redis.ConnectionError:
    raise RuntimeError("Failed to connect to Redis.")  # raise, don't return jsonify

except redis.RedisError as e:
    raise RuntimeError(f"Redis error: {str(e)}")

except Exception as e:
    raise RuntimeError(f"Unexpected error: {str(e)}")

@kv_bp.route("/by-sid", methods=["POST"])
@rate_limit(limit=10,window=3600)  # 10 requests per hour
@require_api_key
def submitnewkv():
    """
    encryption endpoint:
    generate new key and get msg encrypted
    or 
    use old key for encryption as well 
    """

    #step 0 
    new_key=request.form.get("key")
    new_msg=request.form.get("msg")
    
    check=HazardProcessor()
    new_key=check.process_all(new_key)
    new_msg=check.process_all(new_msg)
    
    #init check or existing key 
    if r.exists(new_key):
        dirty_pass_dict = r.hgetall(new_key)
        if not dirty_pass_dict:
            return jsonify({"error": "key not found, generate new "}), 404
        pass_dict = {k.decode(): v.decode() for k, v in dirty_pass_dict.items()}
        
        
        #step 2  - getting teh msg encoded  
        encoded_msg=encoder(new_msg,pass_dict)
        
        # Step 3 and 4: Redis operations
        try:
            # Get hash and redis key for encoded message
            hash_to_user = finalandsigner(encoded_msg)

            # Store the encoded message mapping
            r.set(hash_to_user,encoded_msg,ex=86400)

        except redis.ConnectionError:
            return jsonify({"error": "Failed to connect to Redis."}), 500

        except redis.RedisError as e:
            return jsonify({"error": f"Redis error: {str(e)}"}), 500

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

        
        #step 5 - return the hashed signed jey to user for open msg 
        return jsonify({"status":"recieved",
                        "your_set_key":f"{new_key} expires after 30 days ",
                        "user_h_s_msg":hash_to_user,
                        "note":"msg is deleted after recieved, if not then auto-deleted in 24-hrs "})
    
    else:
            
        # step 1 - get teh fresh password dictinory 
        fresh_pass_dict=shuffler() 
        
        #step 2  - getting teh msg encoded  
        encoded_msg=encoder(new_msg,fresh_pass_dict)
        
        # Step 3 and 4: Redis operations
        # Store the fresh dict
        r.hset(name=new_key, mapping=fresh_pass_dict)
        r.expire(new_key, 2592000)

        # Get hash and redis key for encoded message
        hash_to_user = finalandsigner(encoded_msg)

        # Store the encoded message mapping
        r.set(hash_to_user,encoded_msg,ex=86400)

        
        #step 5 - return the hashed signed jey to user for open msg 
        return jsonify({"status":"recieved",
                        "your_set_key":f"{new_key} expires after 30 days ",
                        "user_h_s_msg":hash_to_user,
                        "note":"msg is deleted after recieved, if not then auto-deleted in 24-hrs "})
