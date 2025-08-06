import face_recognition
import os
import json

def match_face(uploaded_file):
    try:
        uploaded_image = face_recognition.load_image_file(uploaded_file)
        uploaded_encodings = face_recognition.face_encodings(uploaded_image)
    except Exception as e:
        return {"status": "error", "message": f"Failed to load uploaded image: {str(e)}"}

    if len(uploaded_encodings) == 0:
        return {"status": "error", "message": "No face found in the uploaded image."}

    uploaded_encoding = uploaded_encodings[0]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reference_dir = os.path.join(script_dir, 'reference_images')

    matches = []

    for filename in os.listdir(reference_dir):
        filepath = os.path.join(reference_dir, filename)
        try:
            reference_image = face_recognition.load_image_file(filepath)
            reference_encodings = face_recognition.face_encodings(reference_image)

            if not reference_encodings:
                continue

            reference_encoding = reference_encodings[0]
            result = face_recognition.compare_faces([reference_encoding], uploaded_encoding, tolerance=0.6)
            distance = face_recognition.face_distance([reference_encoding], uploaded_encoding)[0]

            if result[0]:
                matches.append({
                    "filename": filename,
                    "confidence": round((1 - distance) * 100, 2)
                })

        except Exception as e:
            continue

    if matches:
        return {"status": "success", "matches": matches}
    else:
        return {"status": "no_match", "message": "No matches found."}
