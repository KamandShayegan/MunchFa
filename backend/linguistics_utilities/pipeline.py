import os
import yaml
import logging
import time
from linguistics_utilities import transcriber, translator, pdf_maker, summarizer

# --- Setup logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Resolve base directory ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# --- Load config.yaml ---
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# --- Construct absolute paths ---
RAW_AUDIO_DIR = os.path.join(BASE_DIR, config["raw_audio_dir"])
EN_DIR = os.path.join(BASE_DIR, config["en_dir"])
GA_DIR = os.path.join(BASE_DIR, config["ga_dir"])
SUMMARY_DIR = os.path.join(BASE_DIR, config["summary_dir"])
PDF_DIR = os.path.join(BASE_DIR, config["pdf_dir"])

# --- Ensure output directories exist ---
for directory in [EN_DIR, GA_DIR, SUMMARY_DIR, PDF_DIR]:
    os.makedirs(directory, exist_ok=True)

def format_duration(seconds: float) -> str:
    """Format duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    minutes = seconds / 60
    return f"{minutes:.1f} minutes"

# --- Core pipeline ---
def run_pipeline(pdf_only=False, index=None):
    if pdf_only:
        if index is None:
            logging.error("If pdf_only=True, you must specify an index.")
            return

        logging.info(f"📄 Re-generating PDF for index {index} only...")
        ga_path = os.path.join(GA_DIR, f"transl_{index}.txt")
        ga_summary_path = os.path.join(GA_DIR, f"summary_ga_{index}.txt")
        
        if not os.path.exists(ga_path):
            logging.error(f"Irish translation not found: {ga_path}")
            return
        if not os.path.exists(ga_summary_path):
            logging.error(f"Irish summary not found: {ga_summary_path}")
            return

        with open(ga_path, 'r') as f:
            irish_txt = f.read()
        with open(ga_summary_path, 'r') as f:
            irish_summary = f.read()

        pdf_path = os.path.join(PDF_DIR, f"transc_ga_{index}.pdf")
        pdf_maker.make_pdf(irish_text=irish_txt, summary_text=irish_summary, output_path=pdf_path)
        logging.info(f"✔ PDF re-generated → transc_ga_{index}.pdf")
        return

    # --- Normal full pipeline ---
    audio_files = sorted([
        f for f in os.listdir(RAW_AUDIO_DIR) if f.endswith('.m4a')
    ])

    if not audio_files:
        logging.warning("No audio files found in raw audio directory.")
        return

    if index is not None:
        # Process single file by index
        audio_file = f"audio_{index}.m4a"
        if audio_file not in audio_files:
            logging.error(f"Audio file not found: {audio_file}")
            return
        logging.info(f"Processing file: {audio_file}")
        audio_path = os.path.join(RAW_AUDIO_DIR, audio_file)
        
        # 1. Transcribe
        start_time = time.time()
        english_txt = transcriber.transcribe(audio_path)
        transcription_time = time.time() - start_time
        en_path = os.path.join(EN_DIR, f"transc_{index}.txt")
        with open(en_path, 'w') as f:
            f.write(english_txt)
        logging.info(f"✔ Transcription saved → transc_{index}.txt (took {format_duration(transcription_time)})")

        # 2. Summarize
        start_time = time.time()
        summary_txt = summarizer.summarize(english_txt)
        summary_time = time.time() - start_time
        summary_path = os.path.join(SUMMARY_DIR, f"summary_{index}.txt")
        with open(summary_path, 'w') as f:
            f.write(summary_txt)
        logging.info(f"✔ Summary saved → summary_{index}.txt (took {format_duration(summary_time)})")

        # 3. Translate both summary and full transcript
        start_time = time.time()
        irish_summary = translator.translate(summary_txt)
        irish_txt = translator.translate(english_txt)
        translation_time = time.time() - start_time
        
        # Save Irish summary
        ga_summary_path = os.path.join(GA_DIR, f"summary_ga_{index}.txt")
        with open(ga_summary_path, 'w') as f:
            f.write(irish_summary)
        logging.info(f"✔ Irish summary saved → summary_ga_{index}.txt")
        
        # Save Irish translation
        ga_path = os.path.join(GA_DIR, f"transl_{index}.txt")
        with open(ga_path, 'w') as f:
            f.write(irish_txt)
        logging.info(f"✔ Translation saved → transl_{index}.txt (took {format_duration(translation_time)})")

        # 4. PDF Export
        pdf_path = os.path.join(PDF_DIR, f"transc_ga_{index}.pdf")
        pdf_maker.make_pdf(irish_text=irish_txt, summary_text=irish_summary, output_path=pdf_path)
        logging.info(f"✔ PDF saved → transc_ga_{index}.pdf\n")
        return

    # Process all files
    logging.info(f"Processing {len(audio_files)} audio file(s)...")
    for audio_file in audio_files:
        if not audio_file.startswith("audio_") or not audio_file.endswith(".m4a"):
            continue
        try:
            idx = int(audio_file.replace("audio_", "").replace(".m4a", ""))
        except ValueError:
            logging.warning(f"⚠ Skipping file with invalid index: {audio_file}")
            continue

        logging.info(f"Processing file: {audio_file}")
        audio_path = os.path.join(RAW_AUDIO_DIR, audio_file)

        # 1. Transcribe
        start_time = time.time()
        english_txt = transcriber.transcribe(audio_path)
        transcription_time = time.time() - start_time
        en_path = os.path.join(EN_DIR, f"transc_{idx}.txt")
        with open(en_path, 'w') as f:
            f.write(english_txt)
        logging.info(f"✔ Transcription saved → transc_{idx}.txt (took {format_duration(transcription_time)})")

        # 2. Summarize
        start_time = time.time()
        summary_txt = summarizer.summarize(english_txt)
        summary_time = time.time() - start_time
        summary_path = os.path.join(SUMMARY_DIR, f"summary_{idx}.txt")
        with open(summary_path, 'w') as f:
            f.write(summary_txt)
        logging.info(f"✔ Summary saved → summary_{idx}.txt (took {format_duration(summary_time)})")

        # 3. Translate both summary and full transcript
        start_time = time.time()
        irish_summary = translator.translate(summary_txt)
        irish_txt = translator.translate(english_txt)
        translation_time = time.time() - start_time
        
        # Save Irish summary
        ga_summary_path = os.path.join(GA_DIR, f"summary_ga_{idx}.txt")
        with open(ga_summary_path, 'w') as f:
            f.write(irish_summary)
        logging.info(f"✔ Irish summary saved → summary_ga_{idx}.txt")
        
        # Save Irish translation
        ga_path = os.path.join(GA_DIR, f"transl_{idx}.txt")
        with open(ga_path, 'w') as f:
            f.write(irish_txt)
        logging.info(f"✔ Translation saved → transl_{idx}.txt (took {format_duration(translation_time)})")

        # 4. PDF Export
        pdf_path = os.path.join(PDF_DIR, f"transc_ga_{idx}.pdf")
        pdf_maker.make_pdf(irish_text=irish_txt, summary_text=irish_summary, output_path=pdf_path)
        logging.info(f"✔ PDF saved → transc_ga_{idx}.pdf\n")



# --- Entrypoint ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-only", action="store_true", help="Only regenerate a PDF")
    parser.add_argument("--index", type=int, help="Index of the file to process")
    args = parser.parse_args()

    run_pipeline(pdf_only=args.pdf_only, index=args.index)
