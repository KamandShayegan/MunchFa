import whisper
import logging
import openai
import yaml
import os

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

# Configure logging once at the module level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load the Whisper model once
logging.info("Loading Whisper model (medium)...")
model = whisper.load_model("medium")
logging.info("Whisper model loaded successfully.")

# Load OpenAI client
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

client = openai.OpenAI(api_key=config["api-key"])

def analyze_consultation_duration(text: str) -> str:
    """
    Analyzes the consultation transcript to determine the actual consultation duration.
    
    Args:
        text (str): The transcribed consultation text.
    
    Returns:
        str: The estimated consultation duration.
    """
    logging.info("Analyzing consultation duration...")
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a veterinary assistant analyzing consultation transcripts. "
                "Based on the content and context of the conversation, estimate the actual "
                "consultation duration."
                "Return only the duration in minutes. If you can't determine the duration, "
                "provide a reasonable estimate based on the content. If it is an estimate, add an estimate symbol or something"
            )
        },
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    duration = response.choices[0].message.content
    logging.info("Duration analysis complete.")
    return duration

def transcribe(audio_path: str) -> str:
    """
    Transcribes an audio file to English text and analyzes consultation duration.
    
    Args:
        audio_path (str): Full path to the .m4a audio file.
    
    Returns:
        str: Transcribed English text with consultation duration.
    """
    logging.info(f"Transcribing: {audio_path}")
    result = model.transcribe(audio_path)
    transcribed_text = result["text"]
    logging.info(f"Finished transcription of: {audio_path}")
    
    # Analyze consultation duration
    duration = analyze_consultation_duration(transcribed_text)
    
    # Add duration to the end of the transcript
    final_text = f"{transcribed_text}\n\nConsultation Duration: {duration}"
    return final_text
