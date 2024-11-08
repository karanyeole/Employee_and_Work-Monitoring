import face_recognition
import cv2
import os

import os
import json
import face_recognition

def trainer(name):
    known_encodings = []
    known_namers = []
    known_dir = r"S:\face detection\person\ajay"  # Change this to the absolute path of your known persons directory

    # Load known persons
    for file in os.listdir(known_dir):
        file_path = os.path.join(known_dir, file)
        if os.path.isfile(file_path):  # Check if the path is a file, not a directory
            img = face_recognition.load_image_file(file_path)
            # Find face encodings only if at least one face is detected
            face_encodings = face_recognition.face_encodings(img)
            if face_encodings:
                img_enc = face_encodings[0]
                known_encodings.append(img_enc)
                known_namers.append(file.split('.')[0])

    # Return the face encodings and names as a tuple
    return known_encodings, known_namers

# Usage
name = "ajay"  # Replace with the appropriate name
encodings, namers = trainer(name)
import cv2
import face_recognition
from datetime import datetime, timedelta

# Initialize a variable to keep track of the last detection time (set to a time in the past)
last_detection_time = datetime.now() - timedelta(seconds=15)  # Assuming no detection in the last 15 seconds
k = 10

# Function to perform face recognition on a given frame
def recognize_faces(frame, known_encodings, known_namers):
    global k
    global last_detection_time  # Use the global variable

    # Find face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Process each face in the frame
    person_detected = False  # Flag to check if a person is detected in the current frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face encoding with known encodings
        results = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
        namer = "Unknown"  # Default namer if no match is found

        for i in range(len(results)):
            if results[i]:
                # Extract a more general label using split
                namer = known_namers[i].split('_')[0]
                # Update the last detection time when a person is detected
                last_detection_time = datetime.now()
                person_detected = True
                break

        # Draw rectangle and label on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, namer, (left + 2, bottom + 20), font, 0.5, (255, 255, 255), 1)

    # Add timestamp to the corner of the video
    cv2.putText(frame, timestamp, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Check if a person is not detected in the current frame
    if not person_detected and datetime.now() - last_detection_time > timedelta(seconds=10):
        print("Person has not been detected for the last", k, " seconds.")
        k += 10
        # Reset the last detection time
        last_detection_time = datetime.now()

    # Reset k to 10 if a person is detected
    if person_detected:
        k = 10

    return frame

# Usage example:
# frame = ... # Capture a frame from the video feed
# encodings, namers = trainer("example_person")  # Obtain encodings and namers using the trainer function
# recognize_faces(frame, encodings, namers)      # Perform recognition on the frame
# Initialize webcam
video_capture = cv2.VideoCapture(0)  # 0 corresponds to the default camera
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Perform face recognition on the frame
    recognize_faces(frame,encodings, namers)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windowsqq
video_capture.release()
cv2.destroyAllWindows()