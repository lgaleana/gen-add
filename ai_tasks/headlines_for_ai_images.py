import json
import re
from typing import Dict, List

from ai import llm
from utils.io import print_system


PROMPT = """
Your goal is to create an ad with the following dimensions: {dimensions}.
You will rely on an AI image generator to create an image for you.

Create a prompt to be used by the AI image generator.
Pick a dimension to map to from this list: 256x256, 512x512, 1024x1024. The AI image will have these dimensions.
Create a headline.
Consider that the headlines will be edited on top of the generated images.

Here is the summary of the website:
{summary}

Generate a JSON in the following format:
```
{{
    "ad_dimension":
    "dimension_to_map":
    "headline":
    "ai_prompt":
}}
```
"""


def generate_headline_and_prompt(summary: str, dimensions: str) -> str:
    return _generate_headline_and_prompt(PROMPT, summary=summary, dimensions=dimensions)


def _generate_headline_and_prompt(prompt: str, **kwargs) -> str:
    print_system("Generating headline for website...")
    instructions = prompt.format(**kwargs)
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages, temperature=0)
