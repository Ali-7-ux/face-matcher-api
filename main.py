from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import face_recognition
import shutil
import os
import uuid

app = FastAPI()

@app.post("/match")
async def match(image: UploadFile = File(...)):
    # Save uploaded file
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        # Load uploaded image
        uploaded_image = face_recognition.load_image_file(temp_filename)
        uploaded_encodings = face_recognition.face_encodings(uploaded_image)

        if not uploaded_encodings:
            return JSONResponse({"status": "no_match", "message": "No face found."}, status_code=200)

        uploaded_encoding = uploaded_encodings[0]

        # Load reference images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        reference_dir = os.path.join(script_dir, "reference_images")
        matches = []

        for filename in os.listdir(reference_dir):
            filepath = os.path.join(reference_dir, filename)
            try:
                ref_img = face_recognition.load_image_file(filepath)
                ref_encodings = face_recognition.face_encodings(ref_img)
                if not ref_encodings:
                    continue

                result = face_recognition.compare_faces([ref_encodings[0]], uploaded_encoding, tolerance=0.6)
                distance = face_recognition.face_distance([ref_encodings[0]], uploaded_encoding)[0]

                if result[0]:
                    matches.append({
                        "filename": filename,
                        "confidence": round((1 - distance) * 100, 2)
                    })
            except:
                continue

        if matches:
            return {"status": "success", "matches": matches}
        else:
            return {"status": "no_match", "message": "No matches found."}
    finally:
        os.remove(temp_filename)
