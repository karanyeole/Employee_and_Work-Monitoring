import cv2
import mediapipe as mp
from datetime import datetime, timedelta
import pickle

# Initialize face detection using MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.9)

# Define global variables for tracking last detection
last_detection_time = datetime.now()  # Ensure the correct datetime is being used
k = 10  # Threshold for no detection warning

def load_known_faces(file_path):
    with open(file_path, "rb") as f:
        known_faces, known_namers = pickle.load(f)
    return known_faces, known_namers

known_faces, known_namers=load_known_faces("employee_images/AjayHonrao.pkl")

def recognize_faces(frame, known_encodings, known_namers, threshold=0.2):
    global k
    global last_detection_time  # Use the global variable

    # Convert the BGR image to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame using MediaPipe
    results = face_detection.process(rgb_frame)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Process each face in the frame
    person_detected = False  # Flag to check if a person is detected in the current frame

    if results.detections:
        for detection in results.detections:
            # Get the bounding box for the detected face
            bboxC = detection.location_data.relative_bounding_box
            h, w, c = frame.shape
            x, y, w, h = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX

            # Simulating face recognition with known_encodings (using simplified logic)
            # Normally, you'd use face embeddings for recognition, but here, we'll use MediaPipe landmarks for demonstration
            namer = "Unknown"  # Default namer if no match is found
            if known_encodings:
                for i, encoding in enumerate(known_encodings):
                    # Simulating matching logic (this should be replaced with actual face recognition)
                    if detection.score[0] >= threshold:  # Only match if the confidence is above the threshold
                        namer = known_namers[i].split('_')[0]  # Extract the name
                        # Update the last detection time when a person is detected
                        last_detection_time = datetime.now()
                        person_detected = True
                        break

            # Place the name (or "Unknown") on the frame near the face
            cv2.putText(frame, namer, (x + 2, y + 20), font, 0.5, (255, 255, 255), 1)

    # Add timestamp to the corner of the video
    cv2.putText(frame, timestamp, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Check if a person is not detected in the current frame
    if not person_detected and datetime.now() - last_detection_time > timedelta(seconds=10):
        print(f"Person has not been detected for the last {k} seconds.")
        k += 10
        # Reset the last detection time
        last_detection_time = datetime.now()

    # Reset k to 10 if a person is detected
    if person_detected:
        k = 10

    return frame

# Example of video capture loop
video_capture = cv2.VideoCapture(0)  # 0 corresponds to the default camera

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Simulate known_encodings and known_namers
    known_encodings = []  # This should contain the known face encodings
    known_namers = []  # This should contain the corresponding names

    # Perform face recognition on the frame with a threshold of 0.6 (you can change this value)
    frame = recognize_faces(frame, known_encodings, known_namers, threshold=0.6)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
