import sqlite3
import face_recognition
import cv2
import pickle
import time
import os 
from datetime import datetime, timedelta


def load_known_faces(pickle_file):
    k=pickle_file
    pickle_file=os.path.join(pickle_file,"known_faces.pkl")
    with open(pickle_file, 'rb') as f:
        known_encodings, known_names = pickle.load(f)
    return known_encodings, known_names,k

def recognize_faces_from_webcam(known_encodings, known_names, is_running,database_path):
    now = datetime.now()
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
                    now = datetime.now()
                    reap = False
                    start_datetime = datetime.combine(datetime.now().date(), start)
                    start_datetime -= timedelta(seconds=10)
                    start = start_datetime.time()
                    end = now.time()
                    absent_duration = (datetime.combine(datetime.now().date(), end) - 
                                       datetime.combine(datetime.now().date(), start)).seconds
                    insert_into_database(database_path, now.date(), start, end, absent_duration)
            else:
                unknown_face_detected = True

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        if unknown_face_detected and time.time() - last_recognition_time > unknown_timeout:
            last_recognition_time = time.time()
            reap = True
            start = now.time()
            now = datetime.now()
        elif not face_recognized and time.time() - last_recognition_time > recognition_timeout:
            last_recognition_time = time.time()
            reap = True
            start = now.time()
            now = datetime.now()

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def insert_into_database(database_path, date, from_time, to_time, absent_duration):
    """Insert the recognition data into the SQLite database."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # Convert datetime.time objects to strings
    from_time_str = from_time.strftime('%H:%M:%S')
    to_time_str = to_time.strftime('%H:%M:%S')
    
    cursor.execute('''
        INSERT INTO report (date, from_time, to_time, absent_for)
        VALUES (?, ?, ?, ?)
    ''', (date, from_time_str, to_time_str, absent_duration))
    
    conn.commit()
    conn.close()
