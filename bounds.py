import cv2
import apriltag
import time


# Initialize AprilTags detector
detector = apriltag.Detector()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set a timer to print the location every 3 seconds
last_print_time = time.time()
print_interval = 3

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Detect AprilTags in frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray)

    # Calculate position of object
    object_pos = None
    detection_id = -1
    detection_family = ''
    for detection in detections:
        # Ignore AprilTags that are too close or too far away
        if detection.tag_id not in range(0, 36):
            continue

        # Draw a circle at the center of the AprilTag
        center = detection.center.astype(int)
        cv2.circle(frame, tuple(center), 5, (0, 255, 0), -1)

        # Calculate position of object
        x, y = center
        object_pos = (int(x), int(y))
        detection_id = detection.tag_id
        detection_family = detection.tag_family


    # Print location of object every 3 seconds
    current_time = time.time()
    if current_time - last_print_time > print_interval and object_pos is not None:
        print("Detected object at position:", object_pos)
        print(detection_id)
        print(detection_family.decode('utf-8'))
        last_print_time = current_time

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()
