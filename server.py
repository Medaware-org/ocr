from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
import os
from dotenv import load_dotenv
from ocr.ocr import read, lang_list

app = Flask(__name__)
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

@app.route('/api/home', methods=['GET'])
def return_home():
    return jsonify({
        'message': 'Hello World!'
    })


img_ext = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')


@app.route('/api/support/img_ext', methods=['GET'])
def get_supported_img_ext():
    return jsonify({"data": img_ext})  # response works


@app.route('/api/ocr/support/languages', methods=['GET'])
def get_supported_ocr_languages():
    return jsonify({"data": lang_list})  # response works


@app.route('/api/ocr', methods=['POST'])
def post_ocr():
    if 'data' not in request.files:
        return "No file part was found", 400

    posted_file = request.files['data']

    if not posted_file.filename.lower().endswith(img_ext):
        return "Invalid file type", 403

    img_bytes = posted_file.read()
    text = read(img_bytes, detail=False)

    return jsonify({"data": text})  # response works


@app.route('/api/cnn', methods=['POST'])
def post_cnn():
    posted_file = request.files['data']  # file
    print(posted_file)
    return jsonify({"data": posted_file.content_type})  # response works


if __name__ == "__main__":
    host = os.getenv("HOST")  # e.g. "127.0.0.1"
    port = int(os.environ.get('PORT', 5000))  # e.g. 4000, default port 5000
    print(f"Server running on  http://{host}:{port}")
    serve(app, host=host, port=port)
    # app.run(debug=True, port=8080) # todo
