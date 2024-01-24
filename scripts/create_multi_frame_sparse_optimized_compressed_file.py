import numpy as np
import random
import gzip


frame_dims = (10, 10, 10, 4)  # Example dimensions (x, y, z, RGBA)
num_frames = 30 * 60 * 5  # Example number of frames

def get_frame_changes(prev_frame, current_frame):
    """
    Identifies and returns changes from prev_frame to current_frame.
    Each frame is represented as a dictionary with keys as indices (x, y, z) and values as RGBA.
    """
    changes = {}
    # Check for changes and new additions
    for index, rgba in current_frame.items():
        if index not in prev_frame or prev_frame[index] != rgba:
            changes[index] = rgba
    # No need to check for deletions if we assume all pixels are accounted for in each frame
    return changes

def apply_changes(base_frame, changes):
    """
    Applies changes to the base_frame. Changes is a dictionary of indices and their new RGBA values.
    """
    updated_frame = base_frame.copy()  # Copy the base frame to avoid modifying the original
    for index, rgba in changes.items():
        updated_frame[index] = rgba
    return updated_frame

def create_frame_with_changes(prev_frame, dims, change_fraction=0.05):
    """
    Simulates frame changes by modifying a small fraction of the previous frame.
    """
    new_frame = prev_frame.copy()
    num_elements = np.prod(dims[:-1])  # Total number of spatial elements
    num_changes = int(num_elements * change_fraction)  # Number of elements to change
    
    all_indices = [(x, y, z) for x in range(dims[0]) for y in range(dims[1]) for z in range(dims[2])]
    change_indices = random.sample(all_indices, num_changes)
    
    for index in change_indices:
        rgba = [random.randint(0, 255) for _ in range(4)]
        # Only add the change if it's actually different (for demonstration)
        if new_frame.get(index, [0, 0, 0, 0]) != rgba:
            new_frame[index] = rgba
    
    return new_frame

def save_frame_changes(frames, filename):
    with gzip.open(filename, 'wb') as f:
        # Metadata: Number of frames and dimensions
        metadata = np.array([len(frames), *frame_dims[:-1]], dtype=np.int32)
        f.write(metadata.tobytes())
        
        # Save the first frame fully
        first_frame_data = frames[0]
        elements_metadata = np.array([len(first_frame_data)], dtype=np.int32)
        f.write(elements_metadata.tobytes())
        for index, rgba in first_frame_data.items():
            data = np.array([*index, *rgba], dtype=np.uint8)
            f.write(data.tobytes())
        
        # For subsequent frames, only save changes if there are any
        for frame_index in range(1, len(frames)):
            frame_changes = get_frame_changes(frames[frame_index-1], frames[frame_index])
            if frame_changes:
                frame_info = np.array([frame_index, len(frame_changes)], dtype=np.int32)
                f.write(frame_info.tobytes())
                for index, rgba in frame_changes.items():
                    data = np.array([*index, *rgba], dtype=np.uint8)
                    f.write(data.tobytes())


def load_frame_changes(filename):
    with gzip.open(filename, 'rb') as f:
        num_frames, *dims = np.frombuffer(f.read(12), dtype=np.int32)
        frames = [{} for _ in range(num_frames)]
        
        num_elements = int(np.frombuffer(f.read(4), dtype=np.int32))
        for _ in range(num_elements):
            element_data = np.frombuffer(f.read(7), dtype=np.uint8).tolist()
            index = tuple(element_data[:3])
            rgba = element_data[3:]
            frames[0][index] = rgba
        
        while True:
            frame_change_info = f.read(8)
            if not frame_change_info:
                break
            frame_index, num_changes = np.frombuffer(frame_change_info, dtype=np.int32)
            for _ in range(num_changes):
                element_data = np.frombuffer(f.read(7), dtype=np.uint8).tolist()
                index = tuple(element_data[:3])
                rgba = element_data[3:]
                frames[frame_index][index] = rgba
    
    for frame_index in range(1, num_frames):
        frames[frame_index] = apply_changes(frames[frame_index-1], frames[frame_index])
    
    return frames



initial_frame = create_frame_with_changes({}, frame_dims, 1)  # 100% change fraction to fill initial frame

# Generate subsequent frames with changes
frames = [initial_frame] * num_frames



save_frame_changes(frames, "frame_changes.dat.gz")
loaded_frames = load_frame_changes("frame_changes.dat.gz")