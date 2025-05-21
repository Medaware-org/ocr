from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
import os
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from dinov2.labels import classes
from dinov2.predict_02 import predict
from ocr.ocr import read, lang_list
from typing import Union


def flask_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/api/home', methods=['GET'])
    def return_home():
        return jsonify({
            'message': 'Hello World!'
        })

    img_ext = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    # todo check if everywhere where img_ext is checked the img_ext aren't hardcoded
    rotation_values = ["0", "90", "180", "270"]

    @app.route('/api/support/img_ext', methods=['GET'])
    def get_supported_img_ext():
        return jsonify({"data": img_ext})  # response works

    @app.route('/api/ocr/support/languages', methods=['GET'])
    def get_supported_ocr_languages():
        return jsonify({"data": lang_list})  # response works

    @app.route('/api/ocr/support/rotation_values', methods=['GET'])
    def get_supported_ocr_rotation_values():
        return jsonify({"data": rotation_values})  # response works

    @app.route('/api/ocr', methods=['POST'])
    def post_ocr():
        if 'data' not in request.files:
            return "No file part was found", 400

        posted_file = request.files['data']
        rotation = request.form.get('rotation')  # if not present .get() returns None

        if not posted_file.filename.lower().endswith(img_ext):
            return "Invalid file type", 403

        if rotation is not None and f"{rotation}" not in rotation_values:
            return f"Invalid rotation! Permitted are these values: {rotation_values}", 403
        # todo rotation
        # print(f"rotation of file {posted_file.filename}:", rotation)
        img_bytes = posted_file.read()
        text = read(img_bytes, detail=False)

        return jsonify({"data": text})  # response works

    @app.route('/api/cnn', methods=['POST'])
    def post_cnn():
        posted_file = request.files['data']  # file

        if not posted_file.filename.lower().endswith(img_ext):
            return "Invalid file type", 403

        img = np.fromfile(posted_file, dtype=np.uint8)
        output, scores = predict(img)
        scores = {key: float(value) for key, value in scores.items()}

        return jsonify({"output": output, "scores": scores})  # response works

    @app.route('/api/cnn/support/labels', methods=['GET'])
    def get_labels_ghs():
        return jsonify({"data": classes})  # response works

    return app


app = flask_app()
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Restrict CORS to specific origins
load_dotenv()  # loading variables from .env file


# JSON DATA - REQUEST
# posted_file = request.json
# posted_file = posted_file['file']

# FORM DATA - REQUEST
# posted_file = request.form['file']

# FILE DATA - REQUEST
# posted_file = request.files['file']



if __name__ == "__main__":
    host = os.getenv("HOST")  # e.g. "127.0.0.1"
    port = int(os.environ.get('PORT', 5000))  # e.g. 4000, default port 5000
    print(f"Server running on  http://{host}:{port}")
    serve(app, host=host, port=port)
    # app.run(debug=True, port=8080) # todo
