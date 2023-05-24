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
    "prompt":
}}
```
"""


def generate_headline_and_prompt(summary: str, dimensions: str) -> Dict[str, str]:
    print_system("Generating headline for website...")
    instructions = PROMPT.format(
        summary=summary,
        dimensions=dimensions,
    )
    messages = [{"role": "user", "content": instructions}]
    return _parse_output(llm.next(messages, temperature=0))


def _parse_output(assistant_message: str) -> Dict[str, str]:
    # Might throw
    match = re.search("({.*})", assistant_message, re.DOTALL)
    json_request = match.group(0)  # type: ignore
    return json.loads(json_request)
