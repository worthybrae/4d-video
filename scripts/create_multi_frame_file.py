import numpy as np
import random

frame_dims = (10, 10, 10, 4)  # Example dimensions (x, y, z, RGBA)
num_frames = 5  # Example number of frames

def create_random_frame(dims):
    frame = np.zeros(dims, dtype=np.uint8)
    for x in range(dims[0]):
        for y in range(dims[1]):
            for z in range(dims[2]):
                frame[x, y, z] = [random.randint(0, 255) for _ in range(4)]
    return frame

frames = [create_random_frame(frame_dims) for _ in range(num_frames)]

def save_frames(frames, filename):
    with open(filename, 'wb') as f:
        # Metadata: Number of frames and dimensions (simple approach)
        metadata = np.array([len(frames), *frame_dims], dtype=np.int32)
        metadata.tofile(f)
        
        # Write each frame
        for frame in frames:
            frame.tofile(f)

# Save the frames to a file
save_frames(frames, "multiframe.dat")

def load_frames(filename):
    with open(filename, 'rb') as f:
        # Read metadata
        metadata = np.fromfile(f, dtype=np.int32, count=5)  # Number of frames + 4 dimension values
        num_frames, *dims = metadata
        
        # Initialize an array to hold the frames
        frames = []
        
        # Read each frame based on the known dimensions
        frame_size = np.prod(dims)
        for _ in range(num_frames):
            frame = np.fromfile(f, dtype=np.uint8, count=frame_size).reshape(dims)
            frames.append(frame)
    return frames

# Load the frames from the file
loaded_frames = load_frames("multiframe.dat")
print(loaded_frames)