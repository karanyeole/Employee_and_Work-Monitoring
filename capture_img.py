import cv2
import os
import sqlite3
import time
import pickle

import face_recognition

def capture_image_stream(name="unknown"):
    output_folder = "employee_images"
    num_images = 25 # Number of images to capture

    # Create folder path
    output_folder = os.path.join(output_folder, name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video capture (webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Failed to access the camera"

    count = 0
    while count < num_images:  # Capture only 10 images
        ret, frame = cap.read()
        if not ret:
            break

        # Save the image
        img_name = f"{name}_{count}.png"
        img_path = os.path.join(output_folder, img_name)
        cv2.imwrite(img_path, frame)  # Save image
        print(f"Image {count + 1} captured.")
        count += 1
        time.sleep(0.5)  # Brief pause before the next image

        # Encode the frame to JPEG and yield the frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Send the frame to the browser with the current image count
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

    # Return the final count after capturing the images
    yield (b'--frame\r\n'
           b'Content-Type: application/json\r\n\r\n' + str(count).encode() + b'\r\n')


def create_face_database(namer):
    known_dir = os.path.join('employee_images', namer)
    pickle_file = os.path.join(known_dir, "known_faces.pkl")
    known_encodings = []
    known_namers = []
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
            else:
                pass
        labels=0
    with open(pickle_file, 'wb') as f:
        pickle.dump((known_encodings, known_namers), f)
    print(f"Known faces saved to '{pickle_file}'")
    output = os.path.join(known_dir,"report.db")
    conn = sqlite3.connect(output)
    cursor = conn.cursor()

    # Create a table for storing leave requests if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS report (
        date DATE,
        from_time TIME,
        to_time TIME,
        absent_for INT
        )
    ''')
    conn.commit()
    conn.close()
    employee = known_dir

    if os.path.exists(employee):
        for file_name in os.listdir(employee):
            file_path = os.path.join(employee, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                os.remove(file_path)