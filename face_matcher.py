import face_recognition
import os
import sys
import json



sys.stdout.reconfigure(encoding='utf-8')


# rest of your code...

# Check if user provided an input image to match
if len(sys.argv) < 2:
    print("❌ Please provide a path to the uploaded image.")
    sys.exit(1)

uploaded_image_path = sys.argv[1]

# Load uploaded image
print(f"🖼️ Loading uploaded image: {uploaded_image_path}")
try:
    uploaded_image = face_recognition.load_image_file(uploaded_image_path)
    uploaded_encodings = face_recognition.face_encodings(uploaded_image)
except Exception as e:
    print(f"❌ Failed to load uploaded image: {e}")
    sys.exit(1)

if len(uploaded_encodings) == 0:
    print("❌ No face found in the uploaded image.")
    sys.exit(0)

uploaded_encoding = uploaded_encodings[0]

# ✅ Fix: Always get absolute reference image path
script_dir = os.path.dirname(os.path.abspath(__file__))
reference_dir = os.path.abspath(os.path.join(script_dir, '..', 'reference_images'))

matches = []

for filename in os.listdir(reference_dir):
    filepath = os.path.join(reference_dir, filename)
    try:
        reference_image = face_recognition.load_image_file(filepath)
        reference_encodings = face_recognition.face_encodings(reference_image)

        if len(reference_encodings) == 0:
            print(f"❌ No face found in: {filename}")
            continue

        reference_encoding = reference_encodings[0]

        result = face_recognition.compare_faces([reference_encoding], uploaded_encoding, tolerance=0.6)
        distance = face_recognition.face_distance([reference_encoding], uploaded_encoding)[0]
        print(f"📏 Distance to {filename}: {distance}")

        if result[0]:
            matches.append({
                "filename": filename,
                "confidence": round((1 - distance) * 100, 2)
            })
            print(f"✅ Match found with: {filename}")

    except Exception as e:
        print(f"⚠️ Error processing {filename}: {e}")
        continue

if matches:
    print(json.dumps({"status": "success", "matches": matches}))
else:
    print(json.dumps({"status": "no_match", "message": "No matches found."}))
