from PIL import Image
import pytesseract
import sys


# Automatically set Tesseract path based on platform
if sys.platform.startswith("win32"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def load_image(image_path):
    """Load an image from the specified path."""
    return Image.open(image_path)


def calculate_crop_box(start_x, start_y, end_x, end_y, img_width, img_height, canvas_width, canvas_height):
    """Calculate crop box based on canvas and image scaling."""
    left, right = min(start_x, end_x), max(start_x, end_x)
    top, bottom = min(start_y, end_y), max(start_y, end_y)
    scale_x, scale_y = img_width / canvas_width, img_height / canvas_height
    return (
        int(left * scale_x),
        int(top * scale_y),
        int(right * scale_x),
        int(bottom * scale_y),
    )


def crop_image(image, crop_box):
    """Crop the image using the specified coordinates."""
    return image.crop(crop_box)


def extract_text_from_image(image, lang="pol"):
    """Extract and return text from an image using Tesseract OCR."""
    return pytesseract.image_to_string(image, lang=lang).strip()
