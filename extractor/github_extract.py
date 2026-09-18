import re

def github_extractor(raw_text):
    #https://www.github.com/sahil07-codes
    #https://github.com/sahil07-codes
    #github.com/sahil07-codes
    string = r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+"
    Github = re.search(string, raw_text)

    if Github:
        Github = Github.group()
    return Github