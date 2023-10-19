import math
import numpy as np
import pygame
import pygame.surfarray as surfarray
import sys

# Initialize Pygame
pygame.init()

# Set the size of the Pygame window
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Initial bounds of the Mandelbrot set
bounds = [-2.0, 1.0, -1.0, 1.0]

# Correct the aspect ratio of the initial bounds
aspect_ratio = width / height
x_center = (bounds[0] + bounds[1]) / 2
y_center = (bounds[2] + bounds[3]) / 2
x_range = (bounds[1] - bounds[0])
y_range = (bounds[3] - bounds[2])
new_y_range = x_range / aspect_ratio  # maintain the aspect ratio of the window

bounds = [
    x_center - x_range / 2,
    x_center + x_range / 2,
    y_center - new_y_range / 2,
    y_center + new_y_range / 2,
]

# Mandelbrot function with smooth coloring
def mandelbrot(c, max_iterations):
    z = c
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1

    if n == max_iterations:
        return max_iterations

    # Smooth the color gradient
    zn = abs(z)
    nu = math.log(math.log(zn) / math.log(2)) / math.log(2)
    n = n + 1 - nu

    return n


# Function to draw the Mandelbrot set
def draw_mandelbrot(surface, bounds, max_iterations):
    width = surface.get_width()
    height = surface.get_height()
    # Create an array with dimensions in the correct order
    array = np.zeros((height, width, 3), dtype=np.uint8)

    for x in range(0, width):
        for y in range(0, height):
            # Convert pixel coordinate to complex number
            c = complex(bounds[0] + (x / width) * (bounds[1] - bounds[0]),
                        bounds[2] + (y / height) * (bounds[3] - bounds[2]))
            # Compute the number of iterations with smoothing
            m = mandelbrot(c, max_iterations)
            
            # Adjust the hue calculation with smooth coloring
            hue = int(360 * m / max_iterations) % 360
            if m == max_iterations:
                hue = 0  # or another value to indicate that the max was reached

            # Define saturation and value
            saturation = 100
            value = 100 if m < max_iterations else 0

            color = pygame.Color(0)
            color.hsva = (hue, saturation, value, 100)

            # Assign the color in the correct order
            array[y][x] = color.r, color.g, color.b  # adjusted to array[y][x]
    # Transpose the array to (width, height, 3) for make_surface
    array = array.transpose((1, 0, 2))

    # Create a new surface from the array
    new_surface = pygame.surfarray.make_surface(array)
    # Blit this new surface onto the original surface
    surface.blit(new_surface, (0, 0))

    print("Completed draw_mandelbrot function.")  # Debug print

# Dynamic max iterations based on zoom level
max_iterations = 10

# Main loop
redraw = True  # control variable to indicate when to redraw
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button clicked, zooming...")  # Debug print

            mx, my = pygame.mouse.get_pos()  # Mouse position in screen coordinates

            # Convert mouse position to complex coordinates, accounting for the size of the current view
            clicked_point = complex(
                bounds[0] + (mx / width) * (bounds[1] - bounds[0]),
                bounds[2] + (my / height) * (bounds[3] - bounds[2])
            )

            # Calculate the new boundaries, keeping the clicked point as the center
            zoom_factor = 4  # determines how much we zoom in
            new_width = (bounds[1] - bounds[0]) / zoom_factor
            new_height = (bounds[3] - bounds[2]) / zoom_factor
            bounds = [
                clicked_point.real - new_width / 2,
                clicked_point.real + new_width / 2,
                clicked_point.imag - new_height / 2,
                clicked_point.imag + new_height / 2,
            ]

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
