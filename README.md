# Attendance-Checker
The provided code is a Flask-based web application that serves as an attendance checker for students using facial recognition. Here's a summary of what the code does:

-It imports necessary modules, including cv2 for computer vision tasks, face_recognition for facial recognition, Flask for creating the web application, and other relevant modules.

-The code initializes a Flask application and sets up an initial database (students_db) to store student information.

-It defines several Flask routes for creating a group, uploading student images, retrieving student information, and checking attendance.

-The /create_group route allows creating a new student group in the students_db database.

-The /upload_image route handles uploading student images for a specific group and stores them in the appropriate directory.

-The /get_students route retrieves the list of students for a given group from the students_db database.

-The /check_attendance route performs the attendance checking process using facial recognition. It captures video frames using cv2, processes the frames to identify faces using face_recognition, compares the faces with stored student images, and calculates confidence scores and delays. It marks students as present or absent based on the confidence scores and the provided threshold.

-The code also includes a Streamlit-based front-end interface for interacting with the Flask API. It allows selecting a group, retrieving and displaying student information, checking attendance, and creating new groups.
