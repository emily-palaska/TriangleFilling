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

# Function that fills a given triangle with the Gouraud shading technique
# Given that the algorithm only handles triangles, non-convex polygons are not considered in the implentation
#
# Input:
#   img: the given canvas with pre-existing shapes
#   vertices: the three points defining the triangle to be shaded
#   vcolors: the colors od the three vertices
#
# Output:
#   update_img: the new canvas with the filled triangle
def g_shading(img, vertices, vcolors):    
    # Calculate the y scanning range
    ymin = min(vertices[0][1], vertices[1][1], vertices[2][1])
    ymax = max(vertices[0][1], vertices[1][1], vertices[2][1])

    # Find the edges of the triangle using the Bresenham Algorithm on every combination of vertices
    active_edges = []
    for i in range(3):
        start = vertices[i % 3]
        end = vertices[(i + 1) % 3]
        active_edges += bresenham_line(start, end)
    
    # Sort the vertices and edges firstly by y and then by x
    active_edges = sorted(active_edges, key=lambda coord: (coord[1], coord[0]))
    sorted_vertices = sorted(vertices, key=lambda coord: (coord[1], coord[0]))
    
    # Get the indices of sorted vertices in the original list
    indices = [vertices.index(vertex) for vertex in sorted_vertices]    
   
    # Use the indices to sort vcolors
    sorted_vcolors = [vcolors[index] for index in indices]

    # Copy the sorted lists back to the original for ease of use
    vertices = sorted_vertices
    vcolors = sorted_vcolors
    
    # Initialize the result image and border colors for each y line
    updated_img = img
    border_colors = [[0.0 for i in range(3)] for j in range(2)]
    
    # Color in the vertices
    for i in range(3):
        [x, y] = vertices[i]
        updated_img[x][y] = vcolors[i]   
    
    # Scan all the y lines in the calculated range
    for y in range(ymin, ymax, 1):
        # Move all the points with the same y into the current edges list
        current_edges = []
        while active_edges[0][1] == y:
            x, _ = active_edges.pop(0)
            current_edges.append(x)
        
        # Skip the lines with only one vertex point
        if len(current_edges) <= 1:
            continue
        
        # Find the two border clors of the scanning line (left on position 0 and right on position 1)
        order = [0, 1] if vertices[1][0] < vertices[2][0] else [1, 0]
        for c in range(3):
            # Decide the points to interpolate based on y
            if y < vertices[1][1]:
                border_colors[order[0]][c] = vector_interp(vertices[0], vertices[1], vcolors[0][c], vcolors[1][c], y, 2)
            else:
                border_colors[order[0]][c] = vector_interp(vertices[1], vertices[2], vcolors[1][c], vcolors[2][c], y, 2)            
            border_colors[order[1]][c] = vector_interp(vertices[0], vertices[2], vcolors[0][c], vcolors[2][c], y, 2)        
        
        # For each pixel in the x scanning range, find the final gouraud color from interpolation
        xmin = current_edges[0]
        xmax = current_edges[-1]
        for x in range(xmin, xmax, 1):
            gouraud_color = [0, 0, 0]
            for i in range(3):
                gouraud_color[i] = vector_interp([xmin, y], [xmax, y], border_colors[0][i], border_colors[1][i], x, 1)
            updated_img[x][y] = gouraud_color
    return updated_img

# Example usage
#M = 1000
#N = 1000
#img = [[[0.99 for i in range(3)] for j in range(N)] for k in range(M)]
#vertices = [[90, 52], [23, 66], [28, 38]]
#vcolors = [[0.83, 0.93, 0.25], [0.33, 0.8, 0.61], [0.03, 0.73, 0.6]]

# Randomize vertices and colors
#vertices = []
#vcolors = []
#for i in range(3):
#  vertices.append([random.randint(0, M - 1), random.randint(0, N - 1)])
#  vcolors.append([random.randint(0, 99) / 100, random.randint(0, 99) / 100, random.randint(0, 99) / 100])print(vertices)print(vcolors)

# Perform the gouraud shading function
#img = g_shading(img, vertices, vcolors)

# Show results
#plt.imshow(img)
#plt.show()
