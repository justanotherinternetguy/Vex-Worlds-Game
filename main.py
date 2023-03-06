import cv2
import apriltag
import pygame
import numpy as np

# Define constants for grid size
GRID_WIDTH = 6
GRID_HEIGHT = 6
TILE_SIZE = 160
GRID_OFFSET_X = 200
GRID_OFFSET_Y = 100

WIDTH = 1920
HEIGHT = 1080

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Arial', 30)

# Initialize AprilTags detector
detector = apriltag.Detector()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create a 6x6 grid of white tiles
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3), dtype=np.uint8)
grid[:] = (255, 255, 255)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    
    # Detect AprilTags in frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray)
    
    # Calculate position of object
    object_pos = None
    for detection in detections:
        # Ignore AprilTags that are too close or too far away
        if detection.tag_id not in range(0, 36):
            continue
        
        # Draw a circle at the center of the AprilTag
        center = detection.center.astype(int)
        cv2.circle(frame, tuple(center), 5, (0, 255, 0), -1)
        
        # Calculate position of object
        x, y = center
        x = (x / WIDTH) * GRID_WIDTH
        y = (y / HEIGHT) * GRID_HEIGHT
        object_pos = (int(x), int(y))
        
    # Update grid to reflect position of object
    if object_pos:
        grid[object_pos[1], object_pos[0]] = (255, 0, 0)
        
    # Draw grid on Pygame screen
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tile_rect = pygame.Rect(GRID_OFFSET_X + x * TILE_SIZE, GRID_OFFSET_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile_color = tuple(grid[y, x])
            pygame.draw.rect(screen, tile_color, tile_rect)
        
    # Draw position text on Pygame screen
    if object_pos:
        text = font.render(f"Object Position: ({object_pos[0]}, {object_pos[1]})", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    
    # Update Pygame display
    pygame.display.update()
    
    # Exit loop if 'q' key is pressed or Pygame window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()




