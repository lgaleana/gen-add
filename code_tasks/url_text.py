"""
ChatGPT-4 prompt: write a python function that given an url returns all text in the website
"""

import requests
from bs4 import BeautifulSoup, Comment

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # remove all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing spaces on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # remove blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text