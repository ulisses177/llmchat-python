import time
import math
import os
import math
import random

from PIL import Image
# Define ASCII characters for different colors
colors = {
    '11': '██',  # White
    '10': '--',  # Light gray
    '01': '--',  # Gray
    '00': '  '   # Black
}



#DEFINE RESOLUTION (16x16)
resX = 12      
resY = 12
deltatime=0.0

def generate_matrix_with_density(old_matrix, density):
    """Generate the next iteration matrix based on the old one and a density parameter."""
    
    # Create a new empty matrix with same dimensions as old_matrix
    new_matrix = [['00' for _ in range(len(old_matrix[0]))] for _ in range(len(old_matrix))] 

    # Iterate over each cell in the old matrix
    for i in range(len(old_matrix)):
        for j in range(len(old_matrix[i])):
            # Randomly decide whether to make this cell live or dead based on density
            if random.random() < density:
                new_matrix[i][j] = '11'  
    return new_matrix

def image_to_positions(image_path):
    """
    Convert an image to a list of positions for ASCII art.

    Args:
    - image_path: Path to the image file.
    - resX: The horizontal resolution of the ASCII art.
    - resY: The vertical resolution of the ASCII art.

    Returns:
    - A list of tuples, where each tuple contains (x, y, color).
    """
    # Open the image
    img = Image.open(image_path)
    # Resize the image to match the ASCII art resolution
    img = img.resize((resX, resY))
    # Convert the image to grayscale
    img = img.convert("L")

    positions = []

    # Iterate over each pixel in the image
    for y in range(resY):
        for x in range(resX):
            # Get the pixel value (0-255)
            pixel_value = img.getpixel((x, y))
            # Map the pixel value to your ASCII art color codes
            if pixel_value > 192:
                color = '11'  # White
            elif pixel_value > 128:
                color = '10'  # Light gray
            elif pixel_value > 64:
                color = '01'  # Gray
            else:
                color = '00'  # Black
            # Append the position and color to the list
            positions.append((x / resX, y / resY, color))

    return positions

def generate_matrix(old_matrix):
    """Generate the next iteration matrix based on the old one."""
    
    # Create a new empty matrix with same dimensions as old_matrix
    new_matrix = [['00' for _ in range(len(old_matrix[0]))] for _ in range(len(old_matrix))] 

    # Iterate over each cell in the old matrix
    for i in range(len(old_matrix)):
        for j in range(len(old_matrix[i])):
            # Count the number of live neighbors
            live_neighbors = count_live_neighbors(old_matrix, i, j)
            
            # Apply Conway's Game of Life rules
            if old_matrix[i][j] == '11':  # Cell is alive
                if live_neighbors < 2 or live_neighbors > 3:  # Underpopulation or overpopulation
                    new_matrix[i][j] = '00'  # The cell dies
                else:  # Otherwise, the cell lives on to the next generation
                    new_matrix[i][j] = '11'  
            elif old_matrix[i][j] == '00':  # Cell is dead
                if live_neighbors == 3:  # Reproduction
                    new_matrix[i][j] = '11'  # A new cell is born
                else:  # Otherwise, the cell remains dead
                    new_matrix[i][j] = '00'  
    return new_matrix

def count_live_neighbors(matrix, x, y):
    """Count the number of live neighbors for a given cell."""
    
    live_neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the current cell itself
            if i == 0 and j == 0:
                continue
            
            # Wrap around edges of matrix
            ni = (x + i) % len(matrix)
            nj = (y + j) % len(matrix[0])
            
            # Increment live_neighbors if neighbor is alive
            if matrix[ni][nj] == '11':
                live_neighbors += 1
    return live_neighbors

# Function to display the matrix
def display_matrix(matrix):
    clear_screen()
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

# Function to generate points in a sine wave
def generate_sine_wave(amplitude, frequency, phase_shift, sincolor, num_points):
    points = []
    for i in range(num_points):
        x = i / num_points  # Normalize x to [0, 1]
        y = amplitude * math.sin(2 * math.pi * frequency * x + phase_shift) + 0.5  # Center y
        y = max(0, min(y, 1))  # Ensure y is clamped between 0 and 1
        points.append((x, y, sincolor))
    return points

# Function to update matrix with positions
def update_matrix(positions):
    new_matrix = [['11' for _ in range(resX)] for _ in range(resY)]  # Initialize with black
    map_positions_to_matrix(positions, new_matrix)  # Update with new positions
    return new_matrix

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')



def generate_circle_points(center_x, center_y, radius):
    points = []
    num_points = int(2 * math.pi * radius * resX)
    if num_points==0:
        num_points+=1
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points  # Angle for this point
        x = center_x + radius * math.cos(angle)  # Calculate x coordinate
        y = center_y + radius * math.sin(angle)  # Calculate y coordinate
        points.append((x, y, '00'))  # Assuming '10' is the color code for these points
    return points

# Example usage

# Now, you can use these points with the rest of your code to map them to the matrix and display them.

# Main function
def main():
    amplitude = 0.4  # Adjust amplitude to fit within the matrix height
    frequency = 2  # Adjust frequency to see the wave within the matrix width
    phase_shift = 0
    num_points = 3*resX  # Generate a point for each column for simplicity
    center_x = 0.1  # Center of the circle, normalized to [0, 1]
    center_y = 0.1  
    radius = 0.4  # Assuming the radius is such that the circle fits in the display
    num_points = int(2 * math.pi * radius * 100)  # Adjust the multiplier for more or fewer points

      # Initialize points4 as an empty list
    points4 = image_to_positions("hammerandsicle.png")
    count = 0
    matrix=update_matrix([])
    #matrix = generate_matrix_with_density(matrix, 0.3)  
    matrix = update_matrix(points4) 
    timestamp=time.process_time()
    deltatime=1
    while True:
        deltatime=time.perf_counter() - timestamp
        time.sleep(05.0)
        print("FPS: ", 1/deltatime)
        #points1 = generate_sine_wave(0.5*amplitude, 2*frequency, 7*phase_shift, '00', num_points)
        #points2 = generate_sine_wave(1*amplitude, 1*frequency, 3*phase_shift+0.25, '01', num_points)
        #points3 = generate_sine_wave(1.5*amplitude, 0.5*frequency, 1*phase_shift+0.5, '10', num_points)
        #matrix = generate_matrix(matrix)
        #timestamp=time.perf_counter()
        
        display_matrix(matrix)
        #phase_shift += 0.016 # Adjust phase shift to animate the wave
        #time.sleep(deltatime)

        

if __name__ == "__main__":
    main()

"""
██████████████▒▒  ░░████████████
██████████████      ████████████
██████████████      ████████████
██████████████      ████████████
██████████░░        ░░▒▒████████
██████████              ▒▒▒▒████
██▒▒  ░░▒▒                  ░░██
██▒▒                        ░░██
████░░                      ░░██
██████                      ░░██
██████▒▒                    ░░██
████████░░                  ░░██
██████████                  ▒▒██
██████████░░                ████
██████████▒▒              ░░████
████████████░░          ░░██████"""