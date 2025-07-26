import redis 
import os
from dotenv import load_dotenv
from ..logics import interpretor
from ..utilities import HazardProcessor
from ..utilities import require_api_key
from flask import request, jsonify, Blueprint 
from ..utilities import rate_limit
from functools import wraps

read_bp = Blueprint("read_bp", __name__)

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

@read_bp.route("/by-sid", methods=["POST"])
@rate_limit(limit=10,window=3600)  # 10 requests per hour
@require_api_key
def read_msg_using_key():
    """
    decryption endpoint:
    use the key to get msd decrypted
    msgs stay for 24 hrs
    and keys are live for 30 days
    """
    # Step 0: Get user inputs
    hmac_msg = request.form.get("secret-msg")
    pass_key = request.form.get("secret-password")
    
    check=HazardProcessor()
    hmac_msg=check.process_all(hmac_msg)
    pass_key=check.process_all(pass_key)
    # Basic validation
    if not hmac_msg or not pass_key:
        return jsonify({"error": "Both secret-msg and secret-password are required"}), 400

    try:

        # Step 2: Fetch encoded message using hmac key
        raw_encoded_msg = r.get(hmac_msg)
        if not raw_encoded_msg:
            raise Exception(" encoded msg not found error ")
        else:
            encoded_msg=raw_encoded_msg.decode()
            

        # Step 3: Fetch password dict using pass_key
        dirty_pass_dict = r.hgetall(pass_key)
        if not dirty_pass_dict:
            return jsonify({"error": "No password dict found for given secret-password"}), 404
        pass_dict = {k.decode(): v.decode() for k, v in dirty_pass_dict.items()}
        
        # Step 4: Decode the message
        final_decoded_msg = interpretor(pass_dict, encoded_msg)
        
        if final_decoded_msg:
            pass
        else:
            raise Exception(" problem in interptitor")
        # Step 5: Delete the message hash from Redis
        r.delete(hmac_msg)

        return jsonify({
            "final_decoded_message": final_decoded_msg,
            "msg_status": "The Message has been permanently deleted",
            "key_status": "You can reuse the password key for future encoding & decoding"
        })

    except redis.RedisError as e:
        return jsonify({"error": f"Redis error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
