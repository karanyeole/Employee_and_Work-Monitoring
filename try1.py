import face_recognition
import cv2
import pickle
import datetime
import time
from datetime import timedelta

def load_known_faces(pickle_file=r"C:\Users\Ajay\OneDrive\Desktop\Interstellar\Employee_and_Work-Monitoring\employee_images\AjayHonrao\known_faces.pkl"):
    with open(pickle_file, 'rb') as f:
        known_encodings, known_names = pickle.load(f)
    return known_encodings, known_names

def recognize_faces_from_webcam(known_encodings, known_names, is_running):
    now = datetime.datetime.now()
    video_capture = cv2.VideoCapture(0)
    reap = False

    last_recognition_time = time.time()
    recognition_timeout = 10
    unknown_timeout = 10

    while is_running():
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_recognized = False
        unknown_face_detected = False

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                last_recognition_time = time.time()
                face_recognized = True
                if reap:
                    now = datetime.datetime.now()
                    reap = False
                    start_datetime = datetime.datetime.combine(datetime.date.today(), start)
                    start_datetime -= timedelta(seconds=10)
                    start = start_datetime.time()
                    end = now.time()
                    print("from", start, "to", end)
            else:
                unknown_face_detected = True

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        if unknown_face_detected and time.time() - last_recognition_time > unknown_timeout:
            last_recognition_time = time.time()
            reap = True
            start = now.time()
            now = datetime.datetime.now()
            print(now.time())
        elif not face_recognized and time.time() - last_recognition_time > recognition_timeout:
            last_recognition_time = time.time()
            reap = True
            start = now.time()
            now = datetime.datetime.now()
            print(now.time())

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
