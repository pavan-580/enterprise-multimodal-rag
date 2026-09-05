import os

import pytesseract
from PIL import Image
from pathlib import Path

from src.error_handler import setup_logging, log_error


setup_logging()

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image
        )

        return text.strip()

    except Exception as error:

        log_error(error)

        return ""