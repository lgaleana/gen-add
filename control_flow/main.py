from ai_tasks.best_headlines import get_headlines
from code_tasks.url_text import get_text_from_url
from utils.io import print_assistant, user_input


def run():
    url = user_input("URL: ")
    text = get_text_from_url(url)
    headlines = get_headlines(text)
    print_assistant(headlines)
