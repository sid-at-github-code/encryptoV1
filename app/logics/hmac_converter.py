import hmac
import hashlib

import os    
from dotenv import load_dotenv

def finalandsigner(encoded_msg:str)->str:
    """
    this takes your one layer encrypted data and 
    1) givens ready dict to put into redis having {hamcIID:encrypted_msg}
    2) final hamc fo user 
    """
    load_dotenv()
    overall_str=os.environ.get("UNIVERSAL_HMAC_KEY")
    if not overall_str:
        raise Exception(" problem with the hamc univeral key ------------------------")
    
    message_bytes = encoded_msg.encode('utf-8')
    secret_key = overall_str.encode('utf-8')

    # HMAC generation
    hmac_hash = hmac.new(secret_key, message_bytes, hashlib.sha256).hexdigest()
    
    to_redis={}
    to_redis[hmac_hash]=encoded_msg
    
    return hmac_hash


if __name__=="__main__":
    blabla="hello sid"
    view_msg=finalandsigner(blabla)
    print(view_msg)