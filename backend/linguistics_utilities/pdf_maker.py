import os
import logging
from weasyprint import HTML

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def make_pdf(persian_text: str, output_path: str):
    """
    Generates a PDF with Persian RTL layout from the given text.
    
    Args:
        persian_text (str): The Persian text content to render.
        output_path (str): Full path where the PDF should be saved.
    """
    logging.info(f"Generating PDF at: {output_path}")

    try:
        # Convert line breaks to <br> for HTML rendering
        content_html = persian_text.replace('\n', '<br>')

        # HTML content with proper styling and font
        html_template = f"""
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
          <meta charset="utf-8">
          <style>
            @font-face {{
              font-family: Vazirmatn;
              src: local("Vazirmatn"), url("https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@latest/dist/Vazirmatn-Regular.woff2") format("woff2");
            }}
            body {{
              font-family: Vazirmatn, sans-serif;
              direction: rtl;
              text-align: right;
              font-size: 16px;
              line-height: 2;
              padding: 2rem;
            }}
          </style>
        </head>
        <body>
          <p>{content_html}</p>
        </body>
        </html>
        """

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate and save the PDF
        HTML(string=html_template).write_pdf(output_path)

        logging.info("PDF generation successful.")

    except Exception as e:
        logging.error(f"Failed to generate PDF: {e}")
        raise
