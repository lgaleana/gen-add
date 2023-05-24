from ai import llm
from utils.io import print_system


PROMPT = """
Here is the text from a website:
{text}

What is this website about?
"""


def summarize_text(text: str) -> str:
    print_system("Summarizing text...")
    instructions = PROMPT.format(text=text)
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages)
