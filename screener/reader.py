import fitz
import logging


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        logging.info("PDF extracted successfully.")
        return text.strip()
    except Exception as e:
        logging.error(f"PDF extraction failed: {e}")
        raise           