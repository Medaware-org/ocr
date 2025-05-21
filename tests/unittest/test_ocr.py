import unittest

from pathlib import Path
from ocr.ocr import read

BASE_DIR = Path(__file__).parent.parent.parent / "ocr"


class OCRUnitTests(unittest.TestCase):
    def test_read_should_not_throw_exception(self):
        try:
            path = BASE_DIR / "images/ocr_ingredient_test_file.jpeg"
            read(f'{path}')
        except Exception as e:
            self.fail(f"function throws an exception but shouldn't: {type(e).__name__}: {e}")

    def test_read_text_should_return_text(self):
        path = BASE_DIR / "images/ocr_ingredient_test_file.jpeg"
        text: list[str] = read(f'{path}')
        print(" ".join(text))
        self.assertTrue(len(text) > 0)


if __name__ == '__main__':
    unittest.main()
