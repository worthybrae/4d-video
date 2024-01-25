from concurrent.futures import ProcessPoolExecutor, as_completed
from helpers.general import generate_random_frame_data, generate_still_frame_data
from tqdm import tqdm
import numpy as np
import gzip


class v4d:
    def __init__(self, width, height, depth, fps):
        self.width = width
        self.height = height
        self.depth = depth
        self.fps = fps
        self.frames = []
        self.header = self.create_header(width, height, depth, 0, fps)  # 0 frames initially

    def create_header(self, width, height, depth, frames, fps):
        return np.array([width, height, depth, frames, fps], dtype=np.int16).tobytes()

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
        
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(generate_still_frame_data, arg) for arg in args]
            
            progress = tqdm(as_completed(futures), total=frames, desc="Generating frames")
            
            for future in progress:
                frame_data = future.result()
                self.add_frame(frame_data)

    def save(self, filename):
        # Use gzip.open to write the file with compression
        with gzip.open(filename, 'wb') as file:
            file.write(self.header)  # Write the header as bytes
            for frame in self.frames:
                file.write(frame.tobytes())


if __name__ == '__main__':
    # Example of usage
    video = v4d(1000, 100, 100, 30)  # Example dimensions and FPS
    video.generate_random_frames()
    video.save('outputs/compressed_try.v4d.gz')
