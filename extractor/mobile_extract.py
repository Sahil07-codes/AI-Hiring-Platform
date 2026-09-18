import re

def mobile_extract(raw_text):

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"
    number = re.search(pattern,raw_text)
    if number:
        return number.group()
    return None
    
    # if type(i)==int:
    #     if i in range(0000000000, 9999999999):
    # return i