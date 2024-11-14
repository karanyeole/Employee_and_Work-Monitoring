import cv2
import os
import numpy as np

# Initialize the OpenCV face detector and face recognizer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Path to the folder where images of the person are stored
image_folder = r'C:\Users\Ajay\OneDrive\Desktop\html study\my project\Interstellar\Employee_and_Work-Monitoring\employee_images\AjayHonrao'
model_file = 'face_model.yml'

def create_face_database(image_folder):
    faces = []
    labels = []
    label = 0  # Label for the person (could be any integer)
    
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

# Create the face database if not already done
if not os.path.exists(model_file):
    print("Model not found. Training the model...")
    create_face_database(image_folder)

# Load the trained model
recognizer.read(model_file)  # Load the pre-trained model
print("Model loaded successfully.")

def recognize_face_from_webcam():
    # Capture video from the webcam
    cap = cv2.VideoCapture(0)  # 0 for default camera
    
    while True:
        # Capture each frame
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Histogram Equalization for better contrast
        gray = cv2.equalizeHist(gray)
        
        # Detect faces in the frame
        faces_in_image = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces_in_image:
            face = gray[y:y+h, x:x+w]
            
            # Use the trained model to predict the label (person)
            label, confidence = recognizer.predict(face)
            
            # Set a higher threshold for confidence to detect an unknown face
            if confidence < 60:  # Adjust threshold here
                cv2.putText(frame, f" {label} (Confidence: {confidence})", 
                            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
            else:
                cv2.putText(frame, "Unknown face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Start face recognition from webcam
recognize_face_from_webcam()
