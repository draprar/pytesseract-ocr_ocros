from PIL import Image
import pytesseract
import os

# Specify Tesseract OCR executable path
TESSERACT_CMD = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def load_image(image_path):
    """Loads an image from the specified path."""
    return Image.open(image_path)


def calculate_crop_box(start_x, start_y, end_x, end_y, img_width, img_height, canvas_width, canvas_height):
    """Calculates the crop box based on coordinates and scaling factors."""
    left = min(start_x, end_x)
    right = max(start_x, end_x)
    top = min(start_y, end_y)
    bottom = max(start_y, end_y)
    scale_x = img_width / canvas_width
    scale_y = img_height / canvas_height
    return (
        int(left * scale_x),
        int(top * scale_y),
        int(right * scale_x),
        int(bottom * scale_y),
    )


def crop_image(image, crop_box):
    """Crops the image using the provided crop box."""
    return image.crop(crop_box)


def extract_text_from_image(image, lang="pol"):
    """Performs OCR on the image and returns cleaned extracted text."""
    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()  # Strip any leading/trailing whitespace or newlines
