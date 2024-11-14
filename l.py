import os
import cv2
import mediapipe as mp
import numpy as np
import warnings

# Suppress all warnings
warnings.filterwarnings('ignore')

# Now proceed with your code
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Function to extract facial landmarks as embeddings
def extract_face_landmarks(image):
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.2, min_tracking_confidence=0.2) as face_mesh:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            face_embedding = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks])
            return face_embedding
        return None

# Function to load known faces from images in a folder
def load_known_faces(folder_path):
    known_face_embeddings = []
    known_face_names = []
    
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = cv2.imread(image_path)
            face_embedding = extract_face_landmarks(image)
            
            if face_embedding is not None:
                known_face_embeddings.append(face_embedding.flatten())  # Flatten the embedding to 1D array
                label = os.path.splitext(filename)[0]  # Use filename as label
                known_face_names.append(label)
                
    return known_face_embeddings, known_face_names

# Function to compare face embeddings using Euclidean distance
def compare_embeddings(embedding1, embedding2):
    distance = np.linalg.norm(embedding1 - embedding2)
    return distance

# Function to recognize faces in real-time from webcam feed
def recognize_faces_in_video(known_face_embeddings, known_face_names):
    cap = cv2.VideoCapture(0)  # Start the webcam feed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        face_embedding = extract_face_landmarks(frame)

        if face_embedding is not None:
            distances = []
            for known_embedding in known_face_embeddings:
                distance = compare_embeddings(face_embedding.flatten(), known_embedding)
                distances.append(distance)

            threshold = 0.6
            min_distance = min(distances)
            if min_distance < threshold:
                matched_index = distances.index(min_distance)
                name = known_face_names[matched_index]
            else:
                name = "Unknown"
            
            if face_embedding is not None:
                with mp_face_mesh.FaceMesh(min_detection_confidence=0.2, min_tracking_confidence=0.2) as face_mesh:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(rgb_frame)
                    if results.multi_face_landmarks:
                        for face_landmarks in results.multi_face_landmarks:
                            h, w, _ = frame.shape
                            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
                            for idx in [0, 4, 10, 5, 195]:
                                x = int(face_landmarks.landmark[idx].x * w)
                                y = int(face_landmarks.landmark[idx].y * h)
                                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                            cv2.putText(frame, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Webcam Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    folder_path = input("Enter the folder path containing the images: ")

    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid path.")
        return

    known_face_embeddings, known_face_names = load_known_faces(folder_path)
    recognize_faces_in_video(known_face_embeddings, known_face_names)

if __name__ == "__main__":
    main()
