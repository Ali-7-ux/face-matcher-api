from flask import Flask, request, jsonify
from flask_cors import CORS
from face_matcher import match_face
import os

app = Flask(__name__)
CORS(app)

@app.route("/match", methods=["POST"])
def match():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image uploaded"}), 400

    uploaded_file = request.files['image']
    result = match_face(uploaded_file)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
