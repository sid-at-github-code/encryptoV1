import re

def encoder(msg:str,fresh_pass_dict:dict)->str:
    """
    takes in teh frshly genrated pass dict
    encodes teh msg using it 
    """
    if re.search(r'[^a-zA-Z0-9 ,. ]',msg):
        raise TypeError(" enter only alphebets,spces and numbers, nohting else allowed ")
    else:
        pass
    msg=msg.lower()
    
    list01=[fresh_pass_dict[i] for i in msg]
    #print(list01) 

    encoded_msg="".join(list01)
    #print("your encoded message is------>")
    return encoded_msg


if __name__ == "__main__":
    # test it here 
    test_dict = {'a': 'e', 'b': 'l', 'c': 'i', 'd': 'k',
                 'e': '.', 'f': '+', 'g': 'b', 'h': 'X',
                 'i': ':', 'j': 'd', 'k': '@', 'l': '^',
                 'm': 'a', 'n': '|', 'o': 'h', 'p': '%',
                 'q': 'm', 'r': 'o', 's': '<', 't': '-',
                 'u': ',', 'v': '_', 'w': '!', 'x': '=',
                 'y': 'c', 'z': '?', '0': 'j', '1': 'p',
                 '2': 'Z', '3': 'g', '4': '/', '5': 'Y',
                 '6': ';', '7': '#', '8': '$', '9': '&', ' ': 'f', '.': '~', ',': '*'}

    msgg ="89, Fa."  # '   ' when decoded
    
    final = encoder(msgg,test_dict)
    print(final)
