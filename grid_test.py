import pygame

# Initialize Pygame
pygame.init()

# Set up the window
screen_width, screen_height = 1080, 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Trapezoid:
    def __init__(self, color, x, y, width, height, slope):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.slope = slope

    def draw(self, surface):
        """Draw the Trapezoid on the surface."""
        # Define the grid
        n_rows, n_cols = 6, 6
        row_height = self.height / n_rows
        col_width = self.width / n_cols
        row_starts = [self.y + i * row_height for i in range(n_rows)]
        col_starts = [self.x + i * col_width for i in range(n_cols)]

        # Draw the Trapezoid and the grid
        points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width - self.slope / 2, self.y + self.height),
            (self.x + self.slope / 2, self.y + self.height),
        ]
        pygame.draw.polygon(surface, self.color, points)
        for row in range(n_rows):
            pygame.draw.line(surface, BLACK, (self.x, row_starts[row]), (self.x + self.width, row_starts[row]))
        for col in range(n_cols):
            pygame.draw.line(surface, BLACK, (col_starts[col], self.y), (col_starts[col], self.y + self.height))


# Create a Trapezoid object
trap = Trapezoid((255, 0, 0), 200, 200, 400, 100, 200)

# Draw the Trapezoid on the screen
trap.draw(screen)

# Update the screen
pygame.display.flip()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()

