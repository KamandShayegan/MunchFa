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
  cd frontend
  python3 -m http.server 8000 
  ```

## 🤖 AI contribution
The user interface is created using ChatGPT-4o. 

## 📂 Directory Structure

- `data/audios/raw/` — Place your raw `.m4a` audio files here.
- `data/transcriptions/en/` — English transcriptions (auto-generated).
- `data/transcriptions/fa/` — Persian translations (auto-generated).
- `frontend/assets/pdfs/` — Generated Persian PDF files.
- `frontend/assets/audio/` — Final audio files for the web interface.
- `frontend/assets/images/` — Art images for the web interface:
  - `intro_0.jpg`, `intro_1.jpg` — Introduction images
  - `art_1.jpg`, `art_2.jpg` — Art piece images
  - `floor_1.jpg`, `floor_2.jpg` — Floor plan images
- `backend/linguistics_utilities/` — Contains processing scripts.
- `backend/config.yaml` — Project configuration (paths, etc).

## 🌐 Web Interface

- Start a local server in the `frontend` directory:
  ```bash
  # Make sure you're in the project root directory
  cd frontend
  python3 -m http.server 8000
  ```
- Access the interface at [http://localhost:8000](http://localhost:8000)
- The grid and art pages are generated dynamically based on the number of processed files and images.

## ⚙️ Personal Setup (if you want to Do It Yourself)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or, for YAML config support
   pip install pyyaml
   ```

2. **Set up configuration:**
   ```bash
   # Copy the example config file
   cp backend/config.yaml.example backend/config.yaml
   ```
   Then edit `backend/config.yaml` to match your directory paths.

## 🔄 Processing Pipeline

1. Place your `.m4a` audio files in `data/audios/raw/`.
2. Run the batch processing script to:
   - Transcribe audio to English (`transc_#.txt`)
   - Translate to Persian (`transl_#.txt`)
   - Generate Persian PDF (`transc_fa_#.pdf`)
3. Output files are named and numbered automatically.

NOTE: If you want to manually change the translation, and only run part of the pipeline that re-creates the
pdf, use this configuration:
```bash 
python backend/main.py --pdf-only --index 3
```

NOTE: If you want to rerun the pipeline only for one index:
```bash 
python backend/main.py --index 3
```

## ⚙️ Configuration

- All paths and settings are managed in `backend/config.yaml`.
- Example:
  ```yaml
  raw_audio_dir: data/audios/raw
  en_dir: data/transcriptions/en
  fa_dir: data/transcriptions/fa
  pdf_dir: frontend/assets/pdfs
  ```
- Image naming convention:
  - Introduction images: `intro_0.jpg`, `intro_1.jpg`
  - Art piece images: `art_1.jpg`, `art_2.jpg`
  - Floor plan images: `floor_1.jpg`, `floor_2.jpg`

## 🙏 Credits
All images and contents are right from "Munch" application, and all the art images are from [here](https://foto.munchmuseet.no/fotoweb/).

