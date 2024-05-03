
import time
import math
import os
import math
import random


from PIL import Image

# ASCII characters used to create the output image
#ASCII_CHARS = [' ', '\'', '.', ':', '-', '=', '+', '#', '%', '@']

# Mapping from color codes to ASCII characters
# Define colors
colors = {
    '00': '██',  # White
    '01': '▒▒',  # Light gray
    '10': '░░',  # Gray
    '11': '  '   # Black
}

# DEFINE RESOLUTION (16x16)
resX = 48
resY = 48
deltatime = 0.01

# Function to display the matrix
def display_matrix(matrix):
    if not all(all(cell in colors for cell in row) for row in matrix):
        raise ValueError("Invalid color code detected")
    for row in matrix:
        for col in row:
            color = col[:2]  # Extract color bits
            char = colors[color]
            print(char, end='')
        print()

# Function to map positions to display matrix
def map_positions_to_matrix(positions, matrix):
    for pos in positions:
        x, y, color = pos
        bx = math.floor(x * resX)  # Ensure x is within the horizontal bounds
        by = math.floor(y * resY)  # Ensure y is within the vertical bounds
        if 0 <= bx < resX and 0 <= by < resY:
            matrix[by][bx] = color  # Corrected indexing here

# Function to generate Mandelbrot fractal positions
def mandelbrot_set(cx, cy, size):
    max_iter = 200
    positions = []
    for y in range(resY):
        for x in range(resX):
            zx, zy = 0, 0
            c = complex(cx + (x - resX / 2) * size / resX, cy + (y - resY / 2) * size / resY)
            for i in range(max_iter):
                if zx * zx + zy * zy >= 4:
                    positions.append((x / resX, y / resY, '11'))  # White color for Mandelbrot set
                    break
                zx, zy = zx * zx - zy * zy + c.real, 2 * zx * zy + c.imag
            else:
                positions.append((x / resX, y / resY, '00'))  # Black color for non-Mandelbrot points
    return positions

# Main function
def main():
    # Initialize the matrix with all black
    matrix = [['00' for _ in range(resX)] for _ in range(resY)]

    # Define Mandelbrot set parameters
    cx, cy = -0.5, 0  # Center of the Mandelbrot set
    size = 3  # Size of the Mandelbrot set

    while True:
        clear_screen()
        # Generate Mandelbrot fractal positions
        mandelbrot_positions = mandelbrot_set(cx, cy, size)

        # Map Mandelbrot positions to the matrix
        map_positions_to_matrix(mandelbrot_positions, matrix)

        # Display the matrix
        display_matrix(matrix)

        # Adjust parameters for next iteration (zooming)
        size *= 0.99  # Zoom in
        cx += 0.001  # Move center slightly

        time.sleep(0.1)  # Adjust sleep time as needed for animation speed

# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def compute_center_of_mass(matrix):
    # Find the coordinates of white and black pixels
    white_pixels = [(x, y) for y, row in enumerate(matrix) for x, cell in enumerate(row) if cell == '11']
    black_pixels = [(x, y) for y, row in enumerate(matrix) for x, cell in enumerate(row) if cell == '00']
    
    # Calculate center of mass for each color
    white_center_x = sum(x for x, y in white_pixels) / len(white_pixels) if white_pixels else resX / 2
    white_center_y = sum(y for x, y in white_pixels) / len(white_pixels) if white_pixels else resY / 2
    black_center_x = sum(x for x, y in black_pixels) / len(black_pixels) if black_pixels else resX / 2
    black_center_y = sum(y for x, y in black_pixels) / len(black_pixels) if black_pixels else resY / 2
    
    return (white_center_x + black_center_x) / 2, (white_center_y + black_center_y) / 2

def update_neighbors(matrix):
    updated_matrix = [row[:] for row in matrix]  # Create a copy of the matrix to avoid in-place modifications
    
    for y in range(1, resY - 1):
        for x in range(1, resX - 1):
            neighbors = [
                matrix[y - 1][x], matrix[y + 1][x],  # Top and bottom neighbors
                matrix[y][x - 1], matrix[y][x + 1]   # Left and right neighbors
            ]
            if '11' in neighbors and '00' in neighbors:
                updated_matrix[y][x] = '10'  # Dark gray
            elif '00' in neighbors and '11' in neighbors:
                updated_matrix[y][x] = '01'  # Light gray
    
    return updated_matrix

def main():
    # Initialize the matrix with all black
    matrix = [['00' for _ in range(resX)] for _ in range(resY)]

    # Define Mandelbrot set parameters
    cx, cy = -0.5, 0  # Center of the Mandelbrot set
    size = 3  # Size of the Mandelbrot set

    while True:
        clear_screen()
        # Generate Mandelbrot fractal positions
        mandelbrot_positions = mandelbrot_set(cx, cy, size)

        # Map Mandelbrot positions to the matrix
        map_positions_to_matrix(mandelbrot_positions, matrix)

        # Update colors based on neighbors
        matrix = update_neighbors(matrix)

        # Display the matrix
        display_matrix(matrix)

        # Compute the center of mass of the edges in the Mandelbrot set
        center_x, center_y = compute_center_of_mass(matrix)

        # Adjust parameters for next iteration (zooming)
        dx = (center_x - resX / 2) / resX  # Calculate the change in x direction
        dy = (center_y - resY / 2) / resY  # Calculate the change in y direction
        ratio = sum(1 for row in matrix for cell in row if cell == '00') / sum(1 for row in matrix for cell in row if cell == '11')
        zoom_speed = 0.1 * ratio  # Adjust zoom speed based on the ratio of black and white pixels

        cx += dx * zoom_speed  # Move center towards the center of mass
        cy += dy * zoom_speed

        size *= 0.99  # Zoom in

        time.sleep(0.1)  # Adjust sleep time as needed for animation speed