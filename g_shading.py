import random
import numpy as np
import matplotlib.pyplot as plt
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
    return np.array(pixels)

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
    ymin = np.min(vertices[:, 1])
    ymax = np.max(vertices[:, 1])
    
    # Find the edges of the triangle using the Bresenham Algorithm on every combination of vertices
    active_edges = bresenham_line(vertices[0, :], vertices[1, :])
    active_edges = np.concatenate([active_edges, bresenham_line(vertices[1, :], vertices[2,:])])
    active_edges = np.concatenate([active_edges, bresenham_line(vertices[2, :], vertices[0,:])])

    # Sort the vertices and edges firstly by y and then by x
    active_edges = active_edges[np.lexsort((active_edges[:, 0], active_edges[:, 1]))]
    sorted_vertices_indexes = np.lexsort((vertices[:, 0], vertices[:, 1]))
    vertices = vertices[sorted_vertices_indexes]
    vcolors = vcolors[sorted_vertices_indexes]
    
    # Initialize the result image and border colors for each y line
    updated_img = img.copy()
    border_colors = np.zeros((2, 3))
    
    # Color in the vertices
    for i in range(3):
        [x, y] = vertices[i]
        updated_img[x, y] = vcolors[i]   
    
    # Scan all the y lines in the calculated range
    for y in range(ymin, ymax, 1):
        # Move all the points with the same y into the current edges list
        current_edges = active_edges[active_edges[:, 1] == y][:, 0]
        
        # Skip the lines with only one vertex point
        if len(current_edges) <= 1:
            continue
        
        # Find the two border clors of the scanning line (left on position 0 and right on position 1)
        order = [0, 1] if vertices[1][0] < vertices[2][0] else [1, 0]
        
        # Decide the points to interpolate based on y
        if y < vertices[1][1]:
            border_colors[order[0]] = [vector_interp(vertices[0], vertices[1], vcolors[0][c], vcolors[1][c], y, 2) for c in range(3)]
        else:
            border_colors[order[0]] = [vector_interp(vertices[1], vertices[2], vcolors[1][c], vcolors[2][c], y, 2) for c in range(3)]           
        border_colors[order[1]] = [vector_interp(vertices[0], vertices[2], vcolors[0][c], vcolors[2][c], y, 2) for c in range(3)]        
        
        # For each pixel in the x scanning range, find the final gouraud color from interpolation
        xmin, xmax = np.min(current_edges), np.max(current_edges)
        for x in range(xmin, xmax, 1):
            gouraud_color = [vector_interp([xmin, y], [xmax, y], border_colors[0][c], border_colors[1][c], x, 1) for c in range(3)]
            updated_img[x][y] = gouraud_color
    return updated_img

# Example usage
#M = 1000
#N = 1000
#img = np.full((M, N, 3), 0.99)
#vertices = [[90, 52], [23, 66], [28, 38]]
#vcolors = [[0.83, 0.93, 0.25], [0.33, 0.8, 0.61], [0.03, 0.73, 0.6]]

# Randomize vertices and colors
#vertices = np.array([[random.randint(0, M - 1), random.randint(0, N - 1)] for i in range(3)])
#vcolors = np.array([[random.randint(0, 99) / 100 for i in range(3)] for j in range(3)])

# Perform the gouraud shading function
#img = g_shading(img, vertices, vcolors)

# Show results
#plt.imshow(img)
#plt.show()
