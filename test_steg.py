import os
import unittest
from PIL import Image
from steg import embed_data, extract_data

class TestSteg(unittest.TestCase):
    def setUp(self):
        # Create a simple white image for testing.
        self.test_input = "test_input.png"
        self.test_output = "test_output.png"
        img = Image.new("RGB", (100, 100), color="white")
        img.save(self.test_input)

    def tearDown(self):
        # Clean up test images.
        if os.path.exists(self.test_input):
            os.remove(self.test_input)
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

    def test_embed_and_extract(self):
        message = b"Test secret"
        embed_data(self.test_input, self.test_output, message)
        extracted = extract_data(self.test_output)
        self.assertEqual(message, extracted)

if __name__ == '__main__':
    unittest.main()
