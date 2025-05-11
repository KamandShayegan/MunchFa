import whisper
import logging

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

def transcribe(audio_path: str) -> str:
    """
    Transcribes an audio file to English text.
    
    Args:
        audio_path (str): Full path to the .m4a audio file.
    
    Returns:
        str: Transcribed English text.
    """
    logging.info(f"Transcribing: {audio_path}")
    result = model.transcribe(audio_path)
    logging.info(f"Finished transcription of: {audio_path}")
    return result["text"]
