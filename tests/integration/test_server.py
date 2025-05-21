import json
import unittest

from server import flask_app
from pathlib import Path
# https://flask.palletsprojects.com/en/stable/testing/

# get the resources folder in the tests folder
resources = Path(__file__).parent.parent / "resources"


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """This is run before every test."""
        self.app = flask_app()
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()  # Flask test client
        self.app.testing = True  # Set testing mode to True

    def test_3_4_ocr_read_text_of_image(self):
        response = self.client.post("/api/ocr", data={
            "rotation": 0,
            "data": ((resources / "ocr_ingredient_test_file.jpeg").open("rb"), "ocr_ingredient_test_file.jpeg"),
        }, content_type='multipart/form-data')

        self.assertTrue(response.status_code == 200)
        data = response.json["data"]
        self.assertTrue(len(data) > 0)

    def test_2_1_ghs_180_deg_rotation(self):
        response = self.client.post("/api/cnn", data={
            "data": (resources / "ghs_test_image_exclamation_mark_rotated_180_degree.jpeg").open("rb"),
        })
        self.assertTrue(response.status_code == 200)
        data = response.json["output"]
        self.assertTrue(data == ["Health Hazard/Hazardous to Ozone Layer"])

    def test_2_2_ghs_360_deg_rotation(self):
        response = self.client.post("/api/cnn", data={
            "data": (resources / "ghs_test_image_exclamation_mark.jpeg").open("rb"),
        })
        self.assertTrue(response.status_code == 200)
        data = response.json["output"]
        self.assertTrue(data == ["Health Hazard/Hazardous to Ozone Layer"])

    def test_2_3_ghs_90_deg_rotation(self):
        response = self.client.post("/api/cnn", data={
            "data": (resources / "ghs_test_image_exclamation_mark_rotated_90_degree.jpeg").open("rb"),
        })
        self.assertTrue(response.status_code == 200)
        self.assertIsNotNone(response.json["output"])


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
