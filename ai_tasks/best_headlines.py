from ai import llm
from utils.io import print_system


PROMPT = """
Here is the text from a website:
{text}

Extract or create the 10 best headlines for an ad about the website.
"""


def get_headlines(text: str) -> str:
    print_system("Generating headlines...")
    instructions = PROMPT.format(text=text)
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages)
