import json
from typing import Dict, List

from ai import llm
from utils.io import print_system


PROMPT = """
Your goal is to find a set of the best images that can be used as ads for a website.
The ads have to be in certain dimensions. The images can be edited or cut.
So you must consider which images would be better suited to fit those dimensions.
You should consider the content of the website. The content of the images has been labeled.
You will create a headline for each ad.

Summary of the website:
{summary}

Image urls, with labels and dimensions:
{images}

Dimensions for the ads: {dimensions}

Use the folliowing format. Each dimension requirement must be represented.

Why the image was chosen:
Url:
Headline:
Image dimensions:
Target dimensions: An image can be a good match for more than one dimension
"""


def get_headlines(summary: str, dimensions: List[str], image_labels: List[Dict]) -> str:
    print_system("Generating headlines for images...")
    instructions = PROMPT.format(
        summary=summary,
        images=json.dumps(image_labels, indent=2),
        dimensions=dimensions,
    )
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages, temperature=0)
