import cv2
import apriltag
import time
import random
import numpy as np


# Row 1 Left: (613, 30)
# Row 1 Left: (774, 30)
# Row 1 Left: (935, 30)
# Row 1 Left: (1096, 30)
# Row 1 Left: (1257, 30)
# Row 1 Right: (1418, 56)

# Row 6 left: (451, 834)
# Row 6 left: (682, 834)
# Row 6 left: (913, 834)
# Row 6 left: (1144, 834)
# Row 6 left: (1375, 834)
# Row 6 right: (1606, 838)

# Row 2 Left: (591, 148)
# Row 2 Right: (1442, 170)

# Row 3 Left: (564, 286)
# Row 3 Right: (1479, 309)

# Row 4 Left: (527, 441)
# Row 4 Right: (1504, 466)

# Row 5 Left: (492, 633)
# Row 5 Right: (1562, 633)


# Initialize AprilTags detector
detector = apriltag.Detector()


# Initialize webcam
cap = cv2.VideoCapture(0)


# Set a timer to print the location every 3 seconds
last_print_time = time.time()
print_interval = 3


# Set camera parameters
fx = 1003.57
fy = 1003.57
cx = 960
cy = 540

# Create intrinsic matrix
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]])


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
   point_det = np.array([])
   for detection in detections:
       # Ignore AprilTags that are too close or too far away
       if detection.tag_id not in range(0, 36):
           continue


       # Draw a circle at the center of the AprilTag
       center = detection.center.astype(int)
       cv2.circle(frame, tuple(center), 5, (0, 255, 0), -1)


       # Calculate position of object
       point_3d = np.array([[0.1397], [0], [0]])  # object is 139.7 mm away from the camera
       rvec = np.zeros((3, 1))  # set rotation vector to zero
       tvec = np.zeros((3, 1))  # set translation vector to zero
       point_2d, _ = cv2.projectPoints(point_3d, rvec, tvec, K, None)
       object_pos = (int(point_2d[0][0][0]), int(point_2d[0][0][1]))
       detection_id = detection.tag_id
       detection_family = detection.tag_family


   # Print location of object every 3 seconds
   current_time = time.time()
   if current_time - last_print_time > print_interval and object_pos is not None:
       print("Detected object at position:", object_pos)
       print("Detection ID:", detection_id)
       print("Detection Family:", detection_family.decode('utf-8'))
       last_print_time = current_time


   # Display the frame
   cv2.imshow('Frame', frame)


   # Exit loop if 'q' key is pressed
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break


# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()
