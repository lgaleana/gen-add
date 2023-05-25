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
{image_infos}

Dimensions for the ad: {dimensions}.

Use the following format.

Why the image was chosen:
Url:
Headline:
Original dimensions:
"""


def get_headline_for_image(
    summary: str, dimensions: str, image_infos: List[Dict]
) -> str:
    print_system("Generating ad from images...")
    instructions = PROMPT.format(
        summary=summary,
        image_infos=json.dumps(image_infos, indent=2),
        dimensions=dimensions,
    )
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages)
