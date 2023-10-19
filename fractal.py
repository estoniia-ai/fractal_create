import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the size of the Pygame window
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Mandelbrot function
def mandelbrot(c, max_iterations):
    print("Running mandelbrot function...")  # Debug print
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1
    print(f"mandelbrot function completed with {n} iterations.")  # Debug print
    return n

# Function to draw the Mandelbrot set
def draw_mandelbrot(surface, bounds, max_iterations):
    print("Starting draw_mandelbrot function...")  # Debug print
    width = surface.get_width()
    height = surface.get_height()
    for x in range(0, width):
        for y in range(0, height):
            # Convert pixel coordinate to complex number
            c = complex(bounds[0] + (x / width) * (bounds[1] - bounds[0]),
                        bounds[2] + (y / height) * (bounds[3] - bounds[2]))
            # Compute the number of iterations
            m = mandelbrot(c, max_iterations)
            
            # The color depends on the number of iterations
            hue = int((360 * m) / max_iterations) % 360  # Ensure hue is within 0-360
            saturation = 100  # Use 100 for full saturation, or adjust as desired
            value = 100 if m < max_iterations else 0  # Adjust if you want a different range of brightness

            color = pygame.Color(0)
            color.hsva = (hue, saturation, value, 100)  # Alpha (transparency) set to 100 (opaque)


            # Set the pixel color
            surface.set_at((x, y), color)
    print("Completed draw_mandelbrot function.")  # Debug print

# Initial bounds of the Mandelbrot set
bounds = [-2.0, 1.0, -1.0, 1.0]

# Dynamic max iterations based on zoom level
max_iterations = 50

# Main loop
redraw = True  # control variable to indicate when to redraw
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button clicked, zooming...")  # Debug print
            # When the mouse is clicked, zoom in
            mx, my = pygame.mouse.get_pos()
            # Convert mouse position to complex coordinates
            cx = bounds[0] + (mx / width) * (bounds[1] - bounds[0])
            cy = bounds[2] + (my / height) * (bounds[3] - bounds[2])
            # Zoom towards the complex coordinates
            bounds = [cx - (bounds[1] - bounds[0]) / 4,
                      cx + (bounds[1] - bounds[0]) / 4,
                      cy - (bounds[3] - bounds[2]) / 4,
                      cy + (bounds[3] - bounds[2]) / 4]
            # Increase max_iterations as we zoom in
            max_iterations = int(max_iterations * 1.5)
            redraw = True  # set redraw to True when zoomed

    if redraw:
        print("Redrawing...")  # Debug print
        # Only draw and update the display if needed
        draw_mandelbrot(screen, bounds, max_iterations)
        pygame.display.flip()
        redraw = False  # reset redraw status

    pygame.time.wait(100)  # Adding a small delay to make the print statements more readable

print("Pygame application terminated.")  # This will not print in normal execution flow
