import json
from typing import Dict, List

from ai import llm
from utils.io import print_system


PROMPT = """
Your goal is to find the best image that can be used as an ad for a website.
The ad must have certain dimensions but the image can be edited or cut.
So you must consider an image that is suited to fit those dimensions after editing.
You should consider the content of the website. The content of the images has been labeled.
You will create a headline for the ad.

Summary of the website:
{summary}

Image urls, with labels and dimensions:
{images}

Dimensions for the ad: {dimensions}.

Use the folliowing format.

Why the image was chosen:
Url:
Headline:
Original dimensions:
"""


def get_headlines_for_images(
    summary: str, dimensions: str, image_labels: List[Dict]
) -> str:
    print_system("Generating ad from images...")
    instructions = PROMPT.format(
        summary=summary,
        images=json.dumps(image_labels, indent=2),
        dimensions=dimensions,
    )
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages)
