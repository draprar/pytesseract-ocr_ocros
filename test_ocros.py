import unittest
from PIL import Image
import ocros_logic
import tempfile
import os


class TestOCRosLogic(unittest.TestCase):

    def setUp(self):
        # Create a temporary image for testing
        self.temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        self.temp_image.close()
        self.image = Image.new("RGB", (100, 100), color="white")
        self.image.save(self.temp_image.name)

    def tearDown(self):
        os.remove(self.temp_image.name)

    def test_load_image(self):
        img = ocros_logic.load_image(self.temp_image.name)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (100, 100))

    def test_calculate_crop_box(self):
        crop_box = ocros_logic.calculate_crop_box(10, 10, 50, 50, 100, 100, 100, 100)
        self.assertEqual(crop_box, (10, 10, 50, 50))

    def test_crop_image(self):
        crop_box = (10, 10, 50, 50)
        cropped_img = ocros_logic.crop_image(self.image, crop_box)
        self.assertEqual(cropped_img.size, (40, 40))

    def test_extract_text_from_image(self):
        text = ocros_logic.extract_text_from_image(self.image, lang="eng")
        # Check if the output is a string (OCR may return an empty string for blank images)
        self.assertIsInstance(text, str)


if __name__ == "__main__":
    unittest.main()
