import cv2
import os
import numpy as np
import time

def capture_image_stream(name="unknown"):
    output_folder = "employee_images"
    num_images = 10  # Number of images to capture

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


def trainer(namer):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    model_file = 'employee_images/face_model.yml'
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = []
    labels = []
    label = namer # Label for the person (could be any integer)
    image_folder = os.path.join("employee_images", namer)
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Histogram Equalization for better contrast
            gray = cv2.equalizeHist(gray)
            
            # Detect faces in the image
            faces_in_image = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces_in_image:
                face = gray[y:y+h, x:x+w]
                faces.append(face)
                labels.append(label)
    # Train the recognizer
    recognizer.train(faces, np.array(labels))
    recognizer.save(model_file)  # Save the trained model
    print("Model trained and saved.")