import cv2
import face_recognition
from flask import Flask, jsonify, request
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import pytz

app = Flask(__name__)

# Initial database
students_db = {
    "group1": [
        {
            "name": "Anas Orkhis",
            "present": False,
            "retards": [],
            "course_start_time": pytz.timezone('America/Montreal').localize(datetime(2023, 6, 22, 15, 0))
        },
        {
            "name": "Elmehdi Arkhis",
            "present": False,
            "retards": [],
            "course_start_time": pytz.timezone('America/Montreal').localize(datetime(2023, 6, 22, 15, 0))
        },
        {
            "name": "Adam Jlil",
            "present": False,
            "retards": [],
            "course_start_time": pytz.timezone('America/Montreal').localize(datetime(2023, 6, 22, 15, 0))
        },
        {
            "name": "Mouad Ilmi",
            "present": False,
            "retards": [],
            "course_start_time": pytz.timezone('America/Montreal').localize(datetime(2023, 6, 22, 15, 0))
        },
        {
            "name": "Dounia Jalal",
            "present": False,
            "retards": [],
            "course_start_time": pytz.timezone('America/Montreal').localize(datetime(2023, 6, 22, 15, 0))
        },
    ],
    # More groups...
}



@app.route('/create_group', methods=['POST'])
def create_group():
    new_group = request.json.get('group')
    if new_group in students_db:
        return jsonify({"error": "Group already exists"}), 400
    students_db[new_group] = []
    return jsonify({"message": f"Group {new_group} created successfully."}), 201

@app.route('/upload_image', methods=['POST'])
def upload_image():
    group = request.form.get('group')
    student_name = request.form.get('student_name')
    image_file = request.files['image_file']
    if group not in students_db:
        return jsonify({"error": "Group not found"}), 404
    filename = secure_filename(image_file.filename)
    if not os.path.exists(f'student_images/{group}'):
        os.makedirs(f'student_images/{group}')
    image_file.save(os.path.join(f'student_images/{group}', f'{student_name}.jpg'))
    return jsonify({"message": f"Image for student {student_name} in group {group} uploaded successfully."}), 200

@app.route('/get_students', methods=['GET'])
def get_students():
    group = request.args.get('group')
    if group not in students_db:
        return jsonify({"error": "Group not found"}), 404
    students = students_db[group]
    return jsonify(students)


@app.route('/check_attendance', methods=['POST'])
def check_attendance():
    group = request.json['group']
    students = students_db.get(group, [])

    cap = cv2.VideoCapture(0)

    # Initialize confidence scores
    for student in students:
        student["confidence_score"] = 0
        student["delay"] = 0  # set delay to 0 by default

    # Capture and process 5 frames
    for _ in range(5):
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return "Failed to capture frame", 500

        unknown_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        for unknown_encoding in unknown_encodings:
            for student in students:
                filename = f'student_images/{group}/{student["name"]}.jpg'
                if not os.path.isfile(filename):
                    continue

                image = face_recognition.load_image_file(filename)
                student_encodings = face_recognition.face_encodings(image)

                # If no encodings could be found for student, return an error
                if len(student_encodings) == 0:
                    return f"No face found in image for student {student['name']}", 400

                student_encoding = student_encodings[0]
                results = face_recognition.compare_faces([student_encoding], unknown_encoding)

                # If face is recognized, increment confidence score
                if results[0]:
                    student["confidence_score"] += 1

                    # Check if student is late
                if datetime.now(pytz.timezone('America/Montreal')) > student["course_start_time"]:
                    time_diff = datetime.now(pytz.timezone('America/Montreal')) - student["course_start_time"]
                    student["delay"] = time_diff.total_seconds()


    cap.release()

    # Mark student as present if confidence score is above threshold
    for student in students:
        if student["confidence_score"] >= 3:  # Set your own threshold
            student["present"] = True
        else:
            student["present"] = False

    return jsonify(students)

# Rest of the Flask endpoints...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
