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

