# 🖼️ Experience Oslo's Munch museum

## 📌 Overview

This project processes audio files into English and Persian transcriptions and generates styled PDF documents. It also provides a web interface for browsing and listening to the processed content. The use case of this system is expressed through Edvard Munch's arts.

## 🛠️ Tools Used

- 🔊 **Whisper + GPT-4o** – Transcribe `.m4a` audio to English, then translate to Persian.
- 🖨️ **WeasyPrint** – Generate RTL Persian PDFs with styled HTML + Vazirmatn font.
- 🖼️ **HTML / CSS / JS** – Responsive RTL UI with a dynamic JSON-powered gallery.
- 📁 **Python Modules** – Modular pipeline (`transcriber`, `translator`, `pdf_maker`) controlled via `config.yaml`.
- 🌐 **Local Server** – Run UI with:
  ```bash
  cd user_interface
  python3 -m http.server 8000 
  ```


## 🤖 AI contribution
The user interface is created using ChatGPT-4o. 

## 📂 Directory Structure

- `assets/audios/raw/` — Place your raw `.m4a` audio files here.
- `assets/transcriptions/en/` — English transcriptions (auto-generated).
- `assets/transcriptions/fa/` — Persian translations (auto-generated).
- `user_interface/assets/pdfs/` — Generated Persian PDF files.
- `user_interface/assets/audio/` — Final audio files for the web interface.
- `user_interface/assets/images/` — Art images for the web interface.
- `linguistics_utilities/` — Contains processing scripts.
- `config.yaml` — Project configuration (paths, etc).

## ⚙️ Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or, for YAML config support
   pip install pyyaml
   ```

2. **Edit `config.yaml`** to match your directory paths if needed.

## 🔄 Processing Pipeline

1. Place your `.m4a` audio files in `assets/audios/raw/`.
2. Run the batch processing script to:
   - Transcribe audio to English (`transc_#.txt`)
   - Translate to Persian (`transl_#.txt`)
   - Generate Persian PDF (`transc_fa_#.pdf`)
3. Output files are named and numbered automatically.

NOTE: If you want to manually change the translation, and only run part of the pipeline that re-creates the
pdf, use this configuration:
```bash 
python linguistics_utilities/pipeline.py --pdf-only --index 3
```
or directly from the root path:
```bash 
python main.py --pdf-only --index 3
```

NOTE: If you want to rerun the pipeline only for one index:
```bash 
python main.py --index 3
```

## 🌐 Web Interface

- Start a local server in the `user_interface` directory:
  ```bash
  cd user_interface
  python3 -m http.server 8000
  ```
- Access the interface at [http://localhost:8000](http://localhost:8000)
- The grid and art pages are generated dynamically based on the number of processed files and images.

## ⚙️ Configuration

- All paths and settings are managed in `config.yaml`.
- Example:
  ```yaml
  RAW_AUDIO_DIR: /path/to/raw/audios/
  EN_TXT_DIR: /path/to/english/transcriptions/
  FA_TXT_DIR: /path/to/persian/translations/
  PDF_DIR: /path/to/pdfs/
  ```

## 🙏 Credits
All images and contents are right from "Munch" application, and all the art images are from [here](https://foto.munchmuseet.no/fotoweb/).

