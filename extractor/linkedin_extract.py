import re

def linkedin_extractor(raw_text):

    string = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"
    Linkedin = re.search(string, raw_text)
    if Linkedin:
        Linkedin = Linkedin.group()
    return Linkedin