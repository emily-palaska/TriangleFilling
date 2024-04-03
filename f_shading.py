import matplotlib.pyplot as plt
import numpy as np
from vector_interp import vector_interp

def print_table(table, M, N):
    for i in range(M):
        for j in range(N):
            print(table[i][j], end="\t")
        print()
        
def bresenham_line(start, end):
    edges = []
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        edges.append([x1, y1])
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return edges


def f_shading(img, vertices, vcolors):
    # Initialize updated image by coping the received image
    updated_img = img
    
    # Calculate the flat color as the vector mean of the triangle vertices' colors
    flat_color = [0, 0, 0]
    for i in range(3):
        flat_color[i] = (vcolors[0][i] + vcolors[1][i] + vcolors[2][i]) / 3
    
    # Extract the dimensions of the image
    M = len(img)
    N = len(img[0])
    
    ymin = min(vertices[0][1], vertices[1][1], vertices[2][1])
    ymax = max(vertices[0][1], vertices[1][1], vertices[2][1])
    xmin = min(vertices[0][0], vertices[1][0], vertices[2][0])
    xmax = max(vertices[0][0], vertices[1][0], vertices[2][0])
    
    # Find edges of triangle using Bresenham Algorithm and sort them based on y
    active_edges = []
    for i in range(3):
        start = vertices[i % 3]
        end = vertices[(i + 1) % 3]
        active_edges += bresenham_line(start, end)
    active_edges = sorted(active_edges, key=lambda coord: coord[1])

    for y in range(ymin, ymax, 1):
        current_edges = []
        cross_count = 0
        
        while active_edges[cross_count][1] == y:            
            current_edges.append(active_edges.pop(cross_count))
            
        current_edges = sorted(current_edges, key=lambda coord: coord[0])
        
        if len(current_edges) == 1:
            x = current_edges[0][0]
            updated_img[x][y] = flat_color
            
        else:
            for x in range(current_edges[0][0], current_edges[-1][0]):
                updated_img[x][y] = flat_color
                
            
                
    
    # Delete after implementation
    # Color the traingle in the original image using the 2d canvas as guideline
    
    for edge in active_edges:
        updated_img[edge[0]][edge[1]] = flat_color
    
    return updated_img

# Example usage:

# Initialize parametes
M = 100
N = 100
vertices = [[10, 10], [90, 90], [25, 50]]
vcolors = [[0.3, 0.2, 0.1], [0.9, 0.3, 0.7], [0.6, 0.1, 0.8]]
img = [[[0.99 for i in range(3)] for i in range(N)] for k in range(M)]

# Perform flat shading function
img = f_shading(img, vertices, vcolors)

# Show results
plt.imshow(img)
plt.show()
        

