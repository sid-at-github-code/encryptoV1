import random

def shuffler():
    """
    it takes nothing reutrns password dict
    each time a fresh dcit of kays and shuffled vals
    
    """
    
    all_keys=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
          'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ',".",","]

    all_vals=['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '=', '+',
          ':', ',', '.', '?', '/', '~', '|', ';', '<', 'k', 'l', 'm', 'o', 'p',
          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'X',"Y","Z"]
    
    shuff_vals=random.sample(all_vals,len(all_vals))
    
    fresh_pass_dict={}
    
    for i in range(len(shuff_vals)):
        fresh_pass_dict[all_keys[i]]=shuff_vals[i]
    
    return fresh_pass_dict

if __name__=="__main__":
    new_pass_dict=shuffler()
    print(new_pass_dict)
    
# main 
# fresh_pass_dict from here jsut import and use shuffler
