import numpy as np
import matplotlib.pyplot as plt
from render_img import render_img

# Load the hw1 file
data = np.load('hw1.npy', allow_pickle=True).item()

# Export the needed data to tables
faces = data['faces']
vertices = data['vertices']
vcolors = data['vcolors']
depth = data['depth']

# Perform the rendering
img = render_img(faces, vertices, vcolors, depth, 'f')

# Show and save the results
plt.imshow(img)
plt.imsave('demo_f.png', img)