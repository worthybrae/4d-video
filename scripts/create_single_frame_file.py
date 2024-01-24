import numpy as np
import random

# Define the dimensions of the frame (for example, 10x10x10)
dims = (10, 10, 10, 4)  # The last dimension is for RGBA values

# Create a frame with random RGBA values
frame = np.zeros(dims, dtype=np.uint8)
for x in range(dims[0]):
    for y in range(dims[1]):
        for z in range(dims[2]):
            # Assign random RGBA values (0-255)
            frame[x, y, z] = [random.randint(0, 255) for _ in range(4)]

def save_frame(frame, filename):
    frame.tofile(filename)

# Example of saving a frame
save_frame(frame, "frame1.dat")

def load_frame(filename, dims):
    return np.fromfile(filename, dtype=np.uint8).reshape(dims)

# Example of loading a frame
loaded_frame = load_frame("frame1.dat", dims)
print(loaded_frame)
