
import cv2
import apriltag
import numpy as np
import yaml
import random

# Initialize AprilTags detector
detector = apriltag.Detector()

# Load camera matrix and distortion coefficients from file
with open("calibration_matrix.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    mtx = np.array(data['camera_matrix'])
    dist = np.array(data['dist_coeff'])

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

# Create black image of same size as webcam frame
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
black_image = np.zeros((768, 1024, 3), np.uint8)

# Create a grid of squares evenly distributed in the black image
square_size = 128
grid_row = 5
grid_col = 7
red_square = random.randint(0, grid_row * grid_col - 1)  # randomly choose a square to turn red
for row in range(grid_row):
    for col in range(grid_col):
        x1 = col * square_size
        y1 = row * square_size
        x2 = x1 + square_size
        y2 = y1 + square_size
        if row * grid_col + col == red_square:
            cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 0, 255), -1)  # turn chosen square red
        else:
            cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 0, 0), 1)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Undistort the image using the camera matrix and distortion coefficients
    undistorted_frame = cv2.undistort(frame, mtx, dist, None)

    # Detect AprilTags in frame
    gray = cv2.cvtColor(undistorted_frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray)

    # Update black image with most recent green square and fill the other squares with green color
    for detection in detections:
      if detection.tag_id not in range(0, 36):
         continue
      center = detection.center.astype(int)
      x1, y1 = center - square_size // 2
      x2, y2 = center + square_size // 2
      cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 255, 0), -1)
      text = f"({center[0]}, {center[1]})"
      cv2.putText(black_image, text, (center[0] - 25, center[1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
                  (255, 255, 255), 2)

      # Check if the green square is within 32 pixels of the red square
      for row in range(grid_row):
         for col in range(grid_col):
            if row * grid_col + col == red_square:
                  red_center = np.array([(col + 0.5) * square_size, (row + 0.5) * square_size])  # center of red square
                  distance = np.linalg.norm(center - red_center)  # Euclidean distance between centers
                  if distance <= 100:
                     if not red_updated:
                        cv2.rectangle(black_image, (x1, y1), (x2, y2), (255, 0, 0), -1)  # change color of red square to blue
                        red_updated = True
                  else:
                     red_updated = False

      # Draw grid of squares
      for row in range(grid_row):
         for col in range(grid_col):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            if row * grid_col + col == red_square:
                  if red_updated:
                     cv2.rectangle(black_image, (x1, y1), (x2, y2), (255, 0, 0), -1)  # draw blue square
                  else:
                     cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 0, 255), -1)  # draw red square
            else:
                  cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 0, 0), 1)  # draw black square

    # Display image
    cv2.imshow('Frame', black_image)
    cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Clear the black image for the next detection
    black_image.fill(0)

    # Redraw the grid of squares
    for row in range(grid_row):
        for col in range(grid_col):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            if row * grid_col + col == red_square:
                cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 0, 255), -1)
            else:
                cv2.rectangle(black_image, (x1, y1), (x2, y2), (0, 0, 0), 1)

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()

