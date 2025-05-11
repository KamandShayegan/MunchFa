import os
import yaml
import logging
from linguistics_utilities import transcriber, translator, pdf_maker

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
FA_DIR = os.path.join(BASE_DIR, config["fa_dir"])
PDF_DIR = os.path.join(BASE_DIR, config["pdf_dir"])

# --- Ensure output directories exist ---
for directory in [EN_DIR, FA_DIR, PDF_DIR]:
    os.makedirs(directory, exist_ok=True)

# --- Core pipeline ---
def run_pipeline(pdf_only=False, index=None):
    if pdf_only:
        if index is None:
            logging.error("If pdf_only=True, you must specify an index.")
            return

        logging.info(f"📄 Re-generating PDF for index {index} only...")
        fa_path = os.path.join(FA_DIR, f"transl_{index}.txt")
        if not os.path.exists(fa_path):
            logging.error(f"Persian translation not found: {fa_path}")
            return

        with open(fa_path, 'r') as f:
            persian_txt = f.read()

        pdf_path = os.path.join(PDF_DIR, f"transc_fa_{index}.pdf")
        pdf_maker.make_pdf(persian_txt, output_path=pdf_path)
        logging.info(f"✔ PDF re-generated → transc_fa_{index}.pdf")
        return

    # --- Normal full pipeline ---
    audio_files = sorted([
        f for f in os.listdir(RAW_AUDIO_DIR) if f.endswith('.m4a')
    ])

    if not audio_files:
        logging.warning("No audio files found in raw audio directory.")
        return

    logging.info(f"Found {len(audio_files)} audio file(s). Starting pipeline...")

    for audio_file in audio_files:
        if not audio_file.startswith("audio_") or not audio_file.endswith(".m4a"):
            continue
        try:
            idx = int(audio_file.replace("audio_", "").replace(".m4a", ""))
        except ValueError:
            logging.warning(f"⚠ Skipping file with invalid index: {audio_file}")
            continue

        if index is not None and idx != index:
            continue


        logging.info(f"[{idx}/{len(audio_files)}] Processing: {audio_file}")
        audio_path = os.path.join(RAW_AUDIO_DIR, audio_file)

        # 1. Transcribe
        english_txt = transcriber.transcribe(audio_path)
        en_path = os.path.join(EN_DIR, f"transc_{idx}.txt")
        with open(en_path, 'w') as f:
            f.write(english_txt)
        logging.info(f"✔ Transcription saved → transc_{idx}.txt")

        # 2. Translate
        persian_txt = translator.translate(english_txt)
        fa_path = os.path.join(FA_DIR, f"transl_{idx}.txt")
        with open(fa_path, 'w') as f:
            f.write(persian_txt)
        logging.info(f"✔ Translation saved → transl_{idx}.txt")

        # 3. PDF Export
        pdf_path = os.path.join(PDF_DIR, f"transc_fa_{idx}.pdf")
        pdf_maker.make_pdf(persian_txt, output_path=pdf_path)
        logging.info(f"✔ PDF saved → transc_fa_{idx}.pdf\n")



# --- Entrypoint ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-only", action="store_true", help="Only regenerate a PDF")
    parser.add_argument("--index", type=int, help="Index of the file to process")
    args = parser.parse_args()

    run_pipeline(pdf_only=args.pdf_only, index=args.index)
