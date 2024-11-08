import os
import cv2
import time
cap = cv2.VideoCapture(0)
def capture_images(cap, output_folder, num_images=10, name="unknown"):
    output_folder=os.path.join(output_folder,name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

capture_images(cap, r"S:\face detection\person", num_images=10, name="ajay")