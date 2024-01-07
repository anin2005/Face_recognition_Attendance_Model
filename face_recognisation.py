import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

# Load known faces
anindas_image = face_recognition.load_image_file("faces/photo_5.jpg")
anikets_image = face_recognition.load_image_file("faces/photo_3.jpg")

anindas_face_encoding = face_recognition.face_encodings(anindas_image)[0]
anikets_face_encoding = face_recognition.face_encodings(anikets_image)[0]

known_face_encodings = [anindas_face_encoding, anikets_face_encoding]
known_face_names = ["Aninda", "Aniket"]

# list of expected students
students = known_face_names.copy()

face_locations = []
face_encodings = []

# Get the current date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}_attendance.csv", "w+", newline="")
lnwriter = csv.writer(f)
lnwriter.writerow(["Name", "Time"])

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognize faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            # Add the text if a person is present
            if name in known_face_names:
                font = cv2.FONT_HERSHEY_COMPLEX
                bottomLeftCornerOfText = (10, 100)
                font_scale = 1.5
                font_color = (255, 0, 0)
                thickness = 3
                line_type = 2
                cv2.putText(frame, f"{name} Present", bottomLeftCornerOfText, font,
                            font_scale, font_color, thickness, line_type)

                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
f.close()
  