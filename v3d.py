from concurrent.futures import ProcessPoolExecutor, as_completed
# from helpers.general import generate_random_frame_data, generate_still_frame_data
from tqdm import tqdm
import numpy as np
import gzip
from scipy.sparse import coo_matrix


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
    return sparse_matrices

class v3d:
    def __init__(self, width, height, depth, fps, ppi):
        self.width = width
        self.height = height
        self.depth = depth
        self.fps = fps
        self.ppi = ppi
        self.frames = []
        self.header = self.create_header(width, height, depth, 0, fps, ppi)  # 0 frames initially

    def create_header(self, width, height, depth, frames, fps, ppi):
        return np.array([width, height, depth, frames, fps, ppi], dtype=np.int16).tobytes()

    def add_frame(self, frame_data):
        if not self.frames:  # If it's the first frame
            self.frames.append(frame_data)
        else:
            # Compare with first frame and add only differences
            diff_frame = self.compare_frames(self.frames[0], frame_data)
            self.frames.append(diff_frame)
        # Update header with new frame count
        self.header = self.create_header(self.width, self.height, self.depth, len(self.frames), self.fps)

    def compare_frames(self, initial_frame, current_frame):
    # Convert the lists to NumPy arrays if they aren't already
        return np.setdiff1d(initial_frame, current_frame)

    def generate_random_frames(self, transparent_ratio=0.95, frames=100):
        args = [(self.width, self.height, self.depth, transparent_ratio) for _ in range(frames)]
        fs = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(generate_still_frame_data, arg) for arg in args]
            progress = tqdm(as_completed(futures), total=frames, desc="Generating frames")
            for future in progress:
                fs.append(future.result())

    def save(self, filename):
        # Use gzip.open to write the file with compression
        with gzip.open(filename, 'wb') as file:
            file.write(self.header)  # Write the header as bytes
            for frame in self.frames:
                file.write(frame.tobytes())

    def load(self, filename):
        with gzip.open(filename, 'rb') as file:
            # Read the header
            header = np.frombuffer(file.read(10), dtype=np.int16)
            width, height, depth, frames, fps, ppi = header

            # Initialize with an empty list of frames
            self.frames = []
            self.width, self.height, self.depth, self.fps, self.ppi = width, height, depth, fps, ppi
            
            # Read and reconstruct each frame
            for _ in range(frames):
                frame_length = np.frombuffer(file.read(8), dtype=np.uint64)[0]
                frame_data = np.frombuffer(file.read(frame_length * 8), dtype=np.uint64)
                self.frames.append(frame_data)

            self.header = self.create_header(width, height, depth, frames, fps)


if __name__ == '__main__':
    # Example of usage
    video = v3d(1000, 1000, 100, 30, 100)  # Example dimensions and FPS
    video.generate_random_frames()
