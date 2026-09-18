import re
# from section import section_detector

string = r"[a-zA-Z0-9%+-.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}"

def email_extract(raw_text):
    data=raw_text
    Email = re.search(string, data)
    if Email:
        Email = Email.group()
    return Email