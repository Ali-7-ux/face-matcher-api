from flask import Flask, request, jsonify
from face_matcher import match_face

app = Flask(__name__)

@app.route('/match', methods=['POST'])
def match():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    matches = match_face(file)
    return jsonify(matches)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
