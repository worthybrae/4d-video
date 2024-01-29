import numpy as np
import gzip


def parse_video_file(filename):
    with gzip.open(filename, 'rb') as file:
        # Read the header
        header = file.readline().decode().strip().split()
        width, height, depth, total_frames, fps = map(int, header)
        
        # Initialize a 3D array for the first frame
        frame_data = np.zeros((depth, height, width, 4), dtype=np.uint8)

        # Read and decompress each frame
        frames = [frame_data]
        for _ in range(total_frames):
            line = file.readline()
            frame_changes = np.frombuffer(line, dtype=np.uint64)
            frame_data = decompress_frame(frame_changes, frame_data, width, height, depth)
            frames.append(frame_data)

    return width, height, depth, total_frames, fps, frames

def decompress_frame(frame_changes, previous_frame, width, height, depth):
    frame_data = previous_frame.copy()
    for value in frame_changes:
        pos_int = value & ((1 << 30) - 1)
        rgba_int = value >> 30
        
        x = pos_int & ((1 << 10) - 1)
        y = (pos_int >> 10) & ((1 << 10) - 1)
        z = (pos_int >> 20) & ((1 << 10) - 1)
        
        r = rgba_int & 255
        g = (rgba_int >> 8) & 255
        b = (rgba_int >> 16) & 255
        a = (rgba_int >> 24) & 255
        
        frame_data[z, y, x] = [r, g, b, a]
    
    return frame_data

def play_video(frames, fps):
    # Render outline of 3d matrix based on 
    pass

# Usage
filename = 'path_to_your_3d_video_file.v4d.gz'
width, height, depth, total_frames, fps, frames = parse_video_file(filename)
play_video(frames, fps)
