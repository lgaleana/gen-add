from ai import image
from ai_tasks.best_headlines import get_headlines
from ai_tasks.image_prompt import generate_prompt
from code_tasks.custom import get_labels_from_images
from code_tasks.images_in_url import get_images_from_url
from code_tasks.text_in_url import get_text_from_url
from utils.io import print_assistant, print_system, user_input


def run():
    url = user_input("URL: ")
    text = get_text_from_url(url)
    images = get_images_from_url(url)
    image_labels = get_labels_from_images(images)

    headlines = get_headlines(text)
    print_assistant(headlines)
    prompt = generate_prompt(text)
    print_assistant(prompt)
    print_system("Generating images...")
    image_urls = image.urls(prompt, n=4)
    print_assistant("\n\n".join(image_urls))
