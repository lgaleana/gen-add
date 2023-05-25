from ai import llm
from utils.io import print_system


PROMPT = """
Here is the text from a website:
{text}

What is this website about?
"""


def summarize_text(text: str) -> str:
    return _summarize_text(PROMPT, text=text)


def _summarize_text(prompt: str, **kwargs) -> str:
    print_system("Summarizing text...")
    instructions = prompt.format(**kwargs)
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages)
