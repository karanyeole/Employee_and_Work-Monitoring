import cv2
import os
import time
import mediapipe as mp
def capture_image_stream(name="unknown"):
    output_folder = "employee_images"
    num_images = 100  # Number of images to capture

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
    known_faces = []
    known_namers = []
    known_dir = os.path.join("employee_images", namer)
    print(namer)
    # Initialize MediaPipe face detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    
    # Process each file in the known directory
    for file in os.listdir(known_dir):
        file_path = os.path.join(known_dir, file)
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            img = cv2.imread(file_path)
            
            # Convert the image to RGB as MediaPipe expects RGB format
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Perform face detection
            results = face_detection.process(rgb_img)
            
            # Check if a face is detected
            if results.detections:
                for detection in results.detections:
                    # Append face data to lists (MediaPipe doesn’t provide encodings)
                    known_faces.append(detection)
                    known_namers.append(file.split('.')[0])

    # Close the MediaPipe session
    face_detection.close()
    
    # Return the face detections and names as a tuple
    return known_faces, known_namers