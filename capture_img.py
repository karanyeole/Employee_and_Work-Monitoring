import cv2
import os
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
    while True:  # This will continuously stream the video
        ret, frame = cap.read()
        if not ret:
            break

        # Save image every frame (or at intervals)
        if count < num_images:
            img_name = f"{name}_{count}.png"
            img_path = os.path.join(output_folder, img_name)
            cv2.imwrite(img_path, frame)  # Save image
            print(f"Image {count + 1} captured.")
            count += 1
            time.sleep(0.5)  # Sleep for a brief period before capturing next frame

        # Encode the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Use the multipart/x-mixed-replace content type to send frames
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
