import cv2
import os
import time

def capture(name="unknown"):
    output_folder = "employee_images"
    num_images = 10  # Make sure it's an integer, not a tuple.
    
    # Create folder path
    output_folder = os.path.join(output_folder, name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video capture (webcam)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return "Failed to access the camera"

    count = 0
    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break
        img_name = f"{name}_{count}.png"
        img_path = os.path.join(output_folder, img_name)
        cv2.imwrite(img_path, frame)
        print(f"Image {count + 1} captured.")
        count += 1
        time.sleep(0.5)

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

    return "Image insertion done successfully"
