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


def get_image_info(url: str) -> Dict:
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = url  # type: ignore

    response = client.label_detection(image=image)  # type: ignore
    labels = [label.description for label in response.label_annotations]
    dimensions = get_image_dimensions(url)
    return {
        "url": url,
        "labels": ", ".join(labels),
        "dimensions": f"{dimensions[0]}x{dimensions[1]}",
    }


def run_parallel_jobs(job, inputs, max: int = 100) -> List[Dict]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(job, inputs[:max]))
