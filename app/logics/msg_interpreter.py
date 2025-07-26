def interpretor(pass_dict:dict,msg:str)->str:
    
    """this takes the dictonary formaed by kv gen and 
    interprites msg  using the key and gives decrypticed value """
    
    reversed_dict = {v: k for k, v in pass_dict.items()}
   
    decoded= "".join(reversed_dict[i] for i in msg)
    
    return decoded


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

    msgg = "$&*f+e~"  # '89, fa.' when decoded
    
    final = interpretor(test_dict, msgg)
    print(final)
