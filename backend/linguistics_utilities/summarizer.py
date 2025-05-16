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

def summarize(english_text: str) -> str:
    """
    Summarizes a pet consultation session transcript, extracting key information.

    Args:
        english_text (str): The input English transcript of the consultation.

    Returns:
        str: A structured summary of the consultation.
    """
    logging.info("Starting consultation summary...")
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a veterinary assistant tasked with summarizing pet consultation sessions. "
                "Extract and organize the following key information:\n"
                "- Next appointment\n"
                "- Consultation duration\n"
                "- Pet's condition and symptoms\n"
                "- Vital signs (if mentioned)\n"
                "- Vaccination status and history\n"
                "- Treatment recommendations\n"

                "Format the summary in a clear, structured way with appropriate headings. If you"
                "don't know something, don't say you don't know. Dont mention the pets name."
            )
        },
        {"role": "user", "content": english_text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    summary = response.choices[0].message.content
    logging.info(" Summary generation complete.")
    return summary 