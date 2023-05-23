from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from google.cloud import vision

from utils.io import print_system


def get_labels_from_image(url: str) -> List[str]:
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = url  # type: ignore

    response = client.label_detection(image=image)  # type: ignore
    return [label.description for label in response.label_annotations]


def get_labels_from_images(urls) -> Dict:
    print_system("Generating labels for images...")
    with ThreadPoolExecutor() as executor:
        labels = list(executor.map(get_labels_from_image, urls))
    return {urls[i]: labels[i] for i, url in enumerate(labels)}
