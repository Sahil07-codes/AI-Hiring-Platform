import re

def info_extract(raw_text):
    info = {
    "Name" : '',
    "Email" : '',
    "Github" : '',
    "Linkedin" : '',
    "Mobile" : ''
    }
    string = r"[a-zA-Z0-9%+-.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}"
    Email = re.search(string, raw_text)
    if Email:
        Email = Email.group()
        info['Email'] = Email


    #https://www.github.com/sahil07-codes
    #https://github.com/sahil07-codes
    #github.com/sahil07-codes
    string = r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+"
    Github = re.search(string, raw_text)
    if Github:
        Github = Github.group()
        info['Github'] = Github


    string = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"
    Linkedin = re.search(string, raw_text)
    if Linkedin:
        Linkedin = Linkedin.group()
        info['Linkedin'] = Linkedin


    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"
    number = re.search(pattern,raw_text)
    if number:
        number = number.group()
        info['Mobile'] = number

    data=raw_text.split()
    name = f'{data[0]} {data[1]}'
    info['Name'] = name
    
    return info