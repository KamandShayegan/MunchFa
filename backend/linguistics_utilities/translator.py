import os
import yaml
import openai
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Determine project root and load config.yaml safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Load OpenAI client once
logging.info("Initializing OpenAI client...")
client = openai.OpenAI(api_key=config["api-key"])
logging.info("OpenAI client initialized.")

def translate(english_text: str) -> str:
    """
    Translates English text to fluent Persian using GPT-4o.

    Args:
        english_text (str): The input English transcript.

    Returns:
        str: The translated Persian text.
    """
    logging.info("Starting translation...")
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional Persian translator. "
                "Translate this English transcript into fluent Irish, preserving structure, quotations, and tone. "
                "Avoid literal translation."
            )
        },
        {"role": "user", "content": english_text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    translated_text = response.choices[0].message.content
    logging.info("Translation complete.")
    return translated_text
