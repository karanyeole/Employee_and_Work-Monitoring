import face_recognition
import cv2

# Load an image using OpenCV
image_path = r"Employee_and_Work-Monitoring\employee_images\AjayHonrao\AjayHonrao_0.png"  # Replace with the path to your image
image = cv2.imread(image_path)

# Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Find all face locations in the image
face_locations = face_recognition.face_locations(rgb_image)

# Draw rectangles around the faces
for face_location in face_locations:
    top, right, bottom, left = face_location
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

# Display the image with detected faces
cv2.imshow("Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
