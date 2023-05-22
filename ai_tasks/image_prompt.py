from ai import llm
from utils.io import print_system


PROMPT = """
Here is the text from a website:
{text}

Generate a prompt to send to a generative AI assistant that will create an image for it.
Don't include people or text.
"""


def generate_prompt(text: str) -> str:
    print_system("Generating prompt for image...")
    instructions = PROMPT.format(text=text)
    messages = [{"role": "user", "content": instructions}]
    return llm.next(messages, temperature=0)
