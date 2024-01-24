frame_dims = (10, 10, 10, 4)  # Example dimensions (x, y, z, RGBA)
num_frames = 5  # Example number of frames

import numpy as np
import random

def create_sparse_frame(dims, non_zero_fraction=0.2):
    """
    Create a sparse frame with a specified fraction of non-zero (random) RGBA values.
    """
    num_elements = np.prod(dims[:-1])  # Total number of spatial elements
    num_non_zero = int(num_elements * non_zero_fraction)  # Number of non-zero elements
    
    # Generate non-zero indices without replacement
    all_indices = [(x, y, z) for x in range(dims[0]) for y in range(dims[1]) for z in range(dims[2])]
    non_zero_indices = random.sample(all_indices, num_non_zero)
    
    # Initialize the frame as a list of tuples: ((x, y, z), (R, G, B, A))
    sparse_frame = []
    for index in non_zero_indices:
        rgba = [random.randint(0, 255) for _ in range(4)]
        sparse_frame.append((index, rgba))
    
    return sparse_frame

frames = [create_sparse_frame(frame_dims) for _ in range(num_frames)]

def save_frames(frames, filename):
    with open(filename, 'wb') as f:
        # Metadata: Number of frames, frame dimensions, and then the data
        metadata = np.array([len(frames), *frame_dims[:-1]], dtype=np.int32)  # Exclude RGBA from dims for metadata
        metadata.tofile(f)
        
        # Write each frame's non-zero elements
        for frame in frames:
            # Store the number of non-zero elements in this frame
            num_non_zero = np.array([len(frame)], dtype=np.int32)
            num_non_zero.tofile(f)
            
            # Flatten and store the indices and values
            for index, rgba in frame:
                element_data = np.array([*index, *rgba], dtype=np.uint8)
                element_data.tofile(f)

def load_frames(filename):
    with open(filename, 'rb') as f:
        # Read metadata
        num_frames, *dims = np.fromfile(f, dtype=np.int32, count=4)
        frames = []
        
        for _ in range(num_frames):
            # Read the number of non-zero elements in this frame
            num_non_zero = int(np.fromfile(f, dtype=np.int32, count=1))
            frame_data = []
            
            for _ in range(num_non_zero):
                # Each element consists of 3 indices (x, y, z) + 4 RGBA values
                element_data = np.fromfile(f, dtype=np.uint8, count=7).tolist()
                index = tuple(element_data[:3])
                rgba = element_data[3:]
                frame_data.append((index, rgba))
            
            frames.append(frame_data)
            
    return frames

# Save the sparse frames to a file
save_frames(frames, "sparse_multiframe.dat")

# Load the sparse frames from the file
loaded_frames = load_frames("sparse_multiframe.dat")
print(loaded_frames)
