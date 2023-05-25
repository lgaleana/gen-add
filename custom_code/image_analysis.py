"""
Code here was custom written, but based on ChatGPT-4.
Example prompt: write a python function that uses an api that given an image returns a text summary of it
"""


from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from dotenv import load_dotenv
from google.cloud import vision

from code_tasks.image_dimensions import get_image_dimensions

load_dotenv()


def analyze_images(images) -> List[Dict]:
    max = 20

    def get_image_info(image_url: str) -> Dict:
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = image_url  # type: ignore

        response = client.label_detection(image=image)  # type: ignore
        labels = [label.description for label in response.label_annotations]
        dimensions = get_image_dimensions(image_url)
        return {
            "url": image_url,
            "labels": ", ".join(labels),
            "dimensions": f"{dimensions[0]}x{dimensions[1]}",
        }

    with ThreadPoolExecutor() as executor:
        return list(executor.map(get_image_info, images[:max]))
