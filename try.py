import face_recognition
import cv2
import pickle
import time

# Function to load known faces from the pickle file
def load_known_faces(pickle_file=r"C:\Users\Ajay\OneDrive\Desktop\Interstellar\Employee_and_Work-Monitoring\employee_images\ff\known_faces.pkl"):
    with open(pickle_file, 'rb') as f:
        known_encodings, known_namers = pickle.load(f)
    return known_encodings, known_namers

# Function to recognize faces from a webcam feed
def recognize_faces_from_webcam(known_encodings, known_namers):
    # Start the webcam
    video_capture = cv2.VideoCapture(0)

    last_recognition_time = time.time()  # Track the time of last recognition
    recognition_timeout = 10  # Timeout threshold in seconds
    unknown_timeout = 10  # Timeout threshold for unknown faces

    while True:
        # Capture a frame from the webcam
        ret, frame = video_capture.read()

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_recognized = False  # Flag to check if a face is recognized
        unknown_face_detected = False  # Flag for unknown faces

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding with the known face encodings
            matches = face_recognition.compare_faces(known_encodings, face_encoding)

            name = "Unknown"  # Default name if no match is found

            # If a match is found, use the name of the matched person
            if True in matches:
                first_match_index = matches.index(True)
                name = known_namers[first_match_index]
                last_recognition_time = time.time()  # Update the recognition time
                face_recognized = True  # A recognized face is found

            else:
                unknown_face_detected = True  # An unknown face is detected

            # Draw a rectangle around the face and label it
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # If no known face is recognized and it's an unknown face, track the time for the alert
        if unknown_face_detected and time.time() - last_recognition_time > unknown_timeout:
            cv2.putText(frame, "Employee is not there since last 10 seconds", (50, 50),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Check if more than 10 seconds have passed since the last face recognition
        elif not face_recognized and time.time() - last_recognition_time > recognition_timeout:
            cv2.putText(frame, "Employee is not there since last 10 seconds", (50, 50),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Display the resulting image
        cv2.imshow('Face Recognition', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close any open windows
    video_capture.release()
    cv2.destroyAllWindows()

# Example usage
known_encodings, known_namers = load_known_faces()  # Load known faces from pickle
recognize_faces_from_webcam(known_encodings, known_namers)  # Start recognizing faces from webcam
