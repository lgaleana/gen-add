import json

from ai import image

# from ai_tasks.best_headlines import get_headlines
from ai_tasks.headlines_for_images import get_headlines
from ai_tasks.image_prompt import generate_prompt
from ai_tasks.text_summary import summarize_text
from code_tasks.custom import get_info_for_images
from code_tasks.images_in_url import get_images_from_url
from code_tasks.text_in_url import get_text_from_url
from utils.io import print_assistant, print_system, user_input


DIMENSIONS = [
    "300x50",
    "300x250",
    "300x600",
    "728x90",
    "160x600",
]


def run():
    # url = user_input("URL: ")
    url = "https://www.beachterracemc.com/"
    print_system("Getting URL data...")
    text = get_text_from_url(url)
    images = get_images_from_url(url)
    image_info = get_info_for_images(images)
    print_system(json.dumps(image_info, indent=2))

    summary = summarize_text(text)
    print_assistant(summary)
    headlines = get_headlines(summary, DIMENSIONS, image_info)
    print_assistant(headlines)

    # headlines = get_headlines(text)
    # print_assistant(headlines)
    # prompt = generate_prompt(text)
    # print_assistant(prompt)
    # print_system("Generating images...")
    # image_urls = image.urls(prompt, n=4)
    # print_assistant("\n\n".join(image_urls))
