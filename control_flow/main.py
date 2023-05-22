from ai import image
from ai_tasks.best_headlines import get_headlines
from ai_tasks.image_prompt import generate_prompt
from code_tasks.url_text import get_text_from_url
from utils.io import print_assistant, print_system, user_input


def run():
    url = user_input("URL: ")
    text = get_text_from_url(url)
    headlines = get_headlines(text)
    print_assistant(headlines)
    prompt = generate_prompt(text)
    print_assistant(prompt)
    print_system("Generating images...")
    image_urls = image.urls(prompt, n=4)
    print_assistant("\n\n".join(image_urls))
