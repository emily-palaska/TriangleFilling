import numpy as np

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

# Function that fills a given triangle with the flat shading technique
# Given that the algorithm only handles triangles, non-convex polygons are not considered in the implentation
#
# Input:
#   img: the given canvas with pre-existing shapes
#   vertices: the three points defining the triangle to be shaded
#   vcolors: the colors od the three vertices
#
# Output:
#   update_img: the new canvas with the filled triangle
def f_shading(img, vertices, vcolors):
    # Calculate the flat color as the vector mean of the vertices' colors
    flat_color = np.mean(vcolors, axis = 0)

    # Calculate the y scanning range
    ymin, ymax = np.min(vertices[:, 1]), np.max(vertices[:, 1])

    # Find the edges of the triangle using the Bresenham Algorithm on every combination of vertices
    active_edges = bresenham_line(vertices[0, :], vertices[1, :])
    active_edges = np.concatenate([active_edges, bresenham_line(vertices[1, :], vertices[2,:])])
    active_edges = np.concatenate([active_edges, bresenham_line(vertices[2, :], vertices[0,:])])
    
    # Sort the edges' pixels by y
    active_edges = active_edges[np.argsort(active_edges[:, 1])]

    # Initialize the result image
    updated_img = img.copy()
    
    # Scan all the y lines in the calculated range
    for y in range(ymin, ymax, 1):
        # Move all the points with the same y into the current edges list
        current_edges = active_edges[active_edges[:, 1] == y][:, 0]

        # Skip the lines with only one point (vertex)
        if len(current_edges) <= 1:
            x = current_edges[0]
            updated_img[x][y] = flat_color
            continue
        
        # Color in every pixel in the x scanning line
        xmin, xmax = np.min(current_edges), np.max(current_edges)
        for x in range(xmin, xmax):
            updated_img[x][y] = flat_color
    return updated_img

# Example usage
#M = 100
#N = 100
#img = [[[1 for i in range(3)] for i in range(N)] for k in range(M)]
#vertices = [[0, 0], [999, 999], [0, 999]]
# vcolors = [[0.9, 0, 0], [0.9, 0, 0], [0.9, 0, 0]]

# Randomize vertices and colors
#vertices = []
#vcolors = []
#for i in range(3):
  #vertices.append([random.randint(0, M - 1), random.randint(0, N - 1)])
  #vcolors.append([random.randint(0, 99) / 100, random.randint(0, 99) / 100, random.randint(0, 99) / 100])

# Perform flat shading function
#img = f_shading(img, vertices, vcolors)

# Show results
#plt.imshow(img)
#plt.show()
