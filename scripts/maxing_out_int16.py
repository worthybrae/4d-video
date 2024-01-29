import numpy as np
from scipy.sparse import coo_matrix


width = 1000
height = 1000
depth = 1000
transparent_ratio = .99
total_pixels = int(width * height * depth * transparent_ratio)
w = np.random.randint(0, high=width, size=total_pixels, dtype=np.uint16)
h = np.random.randint(0, high=height, size=total_pixels, dtype=np.uint16)
d = np.random.randint(0, high=depth, size=total_pixels, dtype=np.uint16)
rgba = np.random.randint(0, high=256, size=total_pixels, dtype=np.uint32)
depths = np.unique(d)
sparse_matrices = []
for depth_layer in depths:
    # Filter coordinates and color values for the current depth layer
    mask = d == depth_layer
    w_layer = w[mask]
    h_layer = h[mask]
    rgba_layer = rgba[mask]
    
    # Create the COO matrix for this depth layer
    # Assuming max width and height are known (max_w, max_h)
    matrix = coo_matrix((rgba_layer, (h_layer, w_layer)), shape=(height, width))
    
    # Store the matrix
    sparse_matrices.append(matrix)
print(sparse_matrices)

    


