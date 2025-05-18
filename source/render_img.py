import numpy as np
from f_shading import f_shading
from g_shading import g_shading


# Function that renders an image by shading all the triangles in order of depth
#
# Input:
#   faces: the 3 vertices of every triangle with indexes corresponding to the position in the vertices table
#   vertices: the vertices coordinates
#   vcolors: the colors of the vertices using the former indexing
#   depth: the depth of each vertex using its indexing in the vertices table
#   shading: the technique used to shade the image, takes values 'f' or 'g'
def render_img(faces, vertices, vcolors, depth, shading):
    # Canvas Initialization
    M = 512
    N = 512
    img = np.full((M, N, 3), 0.99)

    # Calculate depth of each triangle
    triangle_depth = np.mean(depth[faces], axis=1)
    
    # Sort the triangle depths and get the indexing
    sorted_depth_indexes = np.argsort(triangle_depth)
    
    # Sort the triangles from the depth indexing
    faces = faces[sorted_depth_indexes]
    
    # Color every triangle in order of depth
    if shading == 'f':
        for t in faces: 
            current_vertices = vertices[t]
            current_colors = vcolors[t]
            img = f_shading(img, current_vertices, current_colors)
    elif shading == 'g':
        for t in faces:
            current_vertices= vertices[t]
            current_colors = vcolors[t]
            img = g_shading(img, current_vertices, current_colors)
    else:
        raise ValueError("Invalid shading. Value should be 'f' or 'g'.")
    return img



