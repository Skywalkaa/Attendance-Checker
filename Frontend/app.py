import streamlit as st
import requests
import os

BACKEND_URL = "http://localhost:5000"
GROUPS = ["group1", "group2", "group3", "group4", "group5"]

st.title("Attendance Checker")

group = st.selectbox("Select the group:", GROUPS)

if st.button("Get Students"):
    response = requests.get(f"{BACKEND_URL}/get_students?group={group}")
    if response.status_code == 200:
        students = response.json()
        st.write("Students:")
        for student in students:
            st.write(f"Name: {student['name']}")
            st.write(f"Presence: {'Present' if student['present'] else 'Absent'}")
            st.write(f"Late: {', '.join(student['retards'])}")
    else:
        st.write("Error retrieving students.")

from datetime import timedelta

if st.button("Check Attendance"):
    data = {"group": group}
    response = requests.post(f"{BACKEND_URL}/check_attendance", json=data)
    if response.status_code == 200:
        attendance_results = response.json()
        st.write("Attendance Results:")
        
        # Prepare table
        table_data = []
        for student in attendance_results:
            hours_late = round(student['delay'] / 3600, 2)
            table_data.append([student['name'], 'Present' if student['present'] else 'Absent', hours_late])
        
        st.table(table_data)
    else:
        st.write("Error checking attendance.")


new_group = st.text_input("Enter the name of the new group to be created:")
if st.button("Create New Group"):
    response = requests.post(f"{BACKEND_URL}/create_group", json={"group": new_group})
    if response.status_code == 200:
        st.write(f"Group {new_group} created successfully.")
        GROUPS.append(new_group)
    else:
        st.write("Error creating group.")

group_to_upload = st.selectbox("Select the group to upload the image:", GROUPS)
student_name = st.text_input("Enter the name of the student:")

# Here you can see that each file uploader now has a unique key argument
uploaded_file1 = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"], key='uploader1')
if st.button("Upload Image1"):
    if uploaded_file1 is not None:
        files = {"image_file": uploaded_file1.getvalue()}
        response = requests.post(f"{BACKEND_URL}/upload_image", files=files, data={"group": group_to_upload, "student_name": student_name})
        if response.status_code == 200:
            st.write(f"Image for student {student_name} in group {group_to_upload} uploaded successfully.")
        else:
            st.write("Error uploading image.")
    else:
        st.write("Please select an image file to upload.")


