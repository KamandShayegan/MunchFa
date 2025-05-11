from linguistics_utilities.pipeline import run_pipeline

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-only", action="store_true", help="Only regenerate a PDF")
    parser.add_argument("--index", type=int, help="Index of the file to process")
    args = parser.parse_args()

    run_pipeline(pdf_only=args.pdf_only, index=args.index)
