import os
import logging
from weasyprint import HTML

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def make_pdf(irish_text: str, summary_text: str, output_path: str):
    """
    Generates a PDF with Irish text layout and consultation summary.
    
    Args:
        irish_text (str): The Irish text content to render.
        summary_text (str): The consultation summary to include.
        output_path (str): Full path where the PDF should be saved.
    """
    logging.info(f"Generating PDF at: {output_path}")

    try:
        # Convert line breaks to <br> for HTML rendering
        content_html = irish_text.replace('\n', '<br>')
        summary_html = summary_text.replace('\n', '<br>')

        # HTML content with proper styling
        html_template = f"""
        <!DOCTYPE html>
        <html lang="ga">
        <head>
          <meta charset="utf-8">
          <style>
            body {{
              font-family: Arial, sans-serif;
              font-size: 16px;
              line-height: 2;
              padding: 2rem;
            }}
            .summary {{
              background-color: #f5f5f5;
              padding: 1rem;
              margin: 1rem 0;
              border-left: 4px solid #4CAF50;
            }}
            h1, h2 {{
              color: #333;
              margin-top: 2rem;
            }}
            .summary h2 {{
              color: #4CAF50;
              margin-top: 0;
            }}
          </style>
        </head>
        <body>
          <h1>Achoimre ar an gComhairle</h1>
          <div class="summary">
            <h2>Eolas Tábhachtach</h2>
            {summary_html}
          </div>
          
          <h1>Taifead Iomlán na Comhairle</h1>
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
