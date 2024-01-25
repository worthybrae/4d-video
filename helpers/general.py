import numpy as np


def generate_random_frame_data(args):
    width, height, depth, transparent_ratio = args
    frame_data = []
    total_pixels = int(width * height * depth * transparent_ratio)
    for _ in range(total_pixels):
        pos = np.array([
            np.random.randint(0, width, dtype=np.uint16),
            np.random.randint(0, height, dtype=np.uint16),
            np.random.randint(0, depth, dtype=np.uint16)
        ])
        rgba = np.random.randint(0, 256, size=4, dtype=np.uint8)

        pos_int = (pos[0] + (pos[1] << 10) + (pos[2] << 20))
        rgba_int = (rgba[0] + (rgba[1] << 8) + (rgba[2] << 16) + (rgba[3] << 24))
        combined_int = pos_int + (rgba_int << 30)

        frame_data.append(combined_int)
    return np.array(frame_data, dtype=np.uint64)

def generate_still_frame_data(args):
    width, height, depth, transparent_ratio = args
    frame_data = []
    total_pixels = int(width * height * depth * transparent_ratio)
    c = 0
    for _ in range(total_pixels):
        pos = np.array([
            c,
            c,
            c
        ], dtype=np.uint16)
        rgba = np.array([100, 100, 100, 100], dtype=np.uint8)

        pos_int = (pos[0] + (pos[1] << 10) + (pos[2] << 20))
        rgba_int = (rgba[0] + (rgba[1] << 8) + (rgba[2] << 16) + (rgba[3] << 24))
        combined_int = pos_int + (rgba_int << 30)

        frame_data.append(combined_int)
        c += 1
    return np.array(frame_data, dtype=np.uint64)