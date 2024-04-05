import matplotlib.pyplot as plt
import random
from vector_interp import vector_interp

# Function that performs the Bresenham Algorithm between two points 
#
# Input: 
#   start: the starting point of the line
#   end: the ending point of the line
#
# Output:
#   pixels: a list of all the pixels in the line connecting the two points
def bresenham_line(start, end):
    # Initialize algorithm by calculating the step and error variables
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    # Loop to decide the next pixel until ending point is reached
    pixels = []
    while True:
        pixels.append([x1, y1])
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return pixels

# Function that fills a given triangle with the flat shading technique
# Given that the algorithm only handles triangles, non-convex polygons are not considered in the implentations
#
# Input:
#   img: the given canvas with pre-existing shapes
#   vertices: the three points defining the triangle to be shaded
#   vcolors: the colors od the three vertices
# Output:
#   update_img: the new canvas with the filled triangle
def g_shading(img, vertices, vcolors):
    # Extract the dimensions of the image
    M = len(img)
    N = len(img[0])

    # Calculate the y scanning range
    ymin = min(vertices[0][1], vertices[1][1], vertices[2][1])
    ymax = max(vertices[0][1], vertices[1][1], vertices[2][1])

    # Find the edges of the triangle using Bresenham Algorithm on every combination of vertices
    active_edges = []
    for i in range(3):
        start = vertices[i % 3]
        end = vertices[(i + 1) % 3]
        active_edges += bresenham_line(start, end)
    
    # Sort the edges' pixels firstly by y and then by x
    active_edges = sorted(active_edges, key=lambda coord: (coord[1], coord[0]))

    # Scann all the y lines in the calculates range
    updated_img = img
    for i in range(3):
        updated_img[vertices[i][0]][vertices[i][1]] = vcolors[i]
        
    for y in range(ymin, ymax, 1):
        # Move all the points with the same y into the current edges list
        current_edges = []
        while active_edges[0][1] == y:
            x, _ = active_edges.pop(0)
            current_edges.append(x)
        
        # Find the two border clors of the scanning line
        border_colors = [[0, 0, 0], [0, 0, 0]]
        for i in range(3):
            border_colors[0][i] = vector_interp(vertices[0], vertices[1], vcolors[0][i], vcolors[1][i], y, 2)
            border_colors[1][i] = vector_interp(vertices[1], vertices[2], vcolors[0][i], vcolors[1][i], y, 2)
    
        # Based on the number of current edges, fill either only one or all the pixels between them
        if len(current_edges) == 1:
            x = current_edges[0]
            updated_img[x][y] = border_colors[0]
        else:
            xmin = current_edges[0]
            xmax = current_edges[-1]
            for x in range(xmin, xmax, 1):
                gouraud_color = [0, 0, 0]
                for i in range(3):
                    gouraud_color[i] = vector_interp([xmin, y], [xmax, y], border_colors[0][i], border_colors[1][i], x, 1)
                updated_img[x][y] = gouraud_color
    return updated_img

# Example usage
M = 10
N = 10
img = [[[0.99 for i in range(3)] for i in range(N)] for k in range(M)]
#vertices = [[0, 0], [999, 999], [0, 999]]
# vcolors = [[0.9, 0, 0], [0.9, 0, 0], [0.9, 0, 0]]

# Randomize vertices and colors
vertices = []
vcolors = []
for i in range(3):
  vertices.append([random.randint(0, M - 1), random.randint(0, N - 1)])
  vcolors.append([random.randint(0, 99) / 100, random.randint(0, 99) / 100, random.randint(0, 99) / 100])

# Perform flat shading function
img = g_shading(img, vertices, vcolors)

# Show results
plt.imshow(img)
plt.show()
