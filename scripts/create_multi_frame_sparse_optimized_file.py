import numpy as np
import random


frame_dims = (10, 10, 10, 4)  # Example dimensions (x, y, z, RGBA)
num_frames = 30 * 60 * 60  # Example number of frames

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
    with open(filename, 'wb') as f:
        # Metadata: Only the number of frames and dimensions are saved initially
        metadata = np.array([len(frames), *frame_dims[:-1]], dtype=np.int32)
        metadata.tofile(f)
        
        # Save the first frame fully
        first_frame_data = frames[0]
        np.array([len(first_frame_data)], dtype=np.int32).tofile(f)  # Number of elements in the first frame
        for index, rgba in first_frame_data.items():
            np.array([*index, *rgba], dtype=np.uint8).tofile(f)
        
        # Check for changes in subsequent frames but skip saving if there are no changes
        for frame_index in range(1, len(frames)):
            frame_changes = get_frame_changes(frames[frame_index-1], frames[frame_index])
            if frame_changes:  # Only save if there are changes
                np.array([frame_index, len(frame_changes)], dtype=np.int32).tofile(f)  # Frame index and number of changes
                for index, rgba in frame_changes.items():
                    np.array([*index, *rgba], dtype=np.uint8).tofile(f)


def load_frame_changes(filename):
    with open(filename, 'rb') as f:
        num_frames, *dims = np.fromfile(f, dtype=np.int32, count=4)
        frames = [{} for _ in range(num_frames)]  # Initialize list of dictionaries for frames
        
        # Load the first frame fully
        num_elements = int(np.fromfile(f, dtype=np.int32, count=1))
        for _ in range(num_elements):
            element_data = np.fromfile(f, dtype=np.uint8, count=7).tolist()
            index = tuple(element_data[:3])
            rgba = element_data[3:]
            frames[0][index] = rgba
        
        # Load changes for subsequent frames
        while True:
            frame_change_info = np.fromfile(f, dtype=np.int32, count=2)
            if frame_change_info.size == 0:
                break  # End of file
            frame_index, num_changes = frame_change_info
            for _ in range(num_changes):
                element_data = np.fromfile(f, dtype=np.uint8, count=7).tolist()
                index = tuple(element_data[:3])
                rgba = element_data[3:]
                frames[frame_index][index] = rgba
    
    # Reconstruct full frames from changes
    for frame_index in range(1, num_frames):
        frames[frame_index] = apply_changes(frames[frame_index-1], frames[frame_index])
    
    return frames

initial_frame = create_frame_with_changes({}, frame_dims, 1)  # 100% change fraction to fill initial frame

frames = [initial_frame] * num_frames
for _ in range(1, num_frames):
    frames.append(create_frame_with_changes(frames[-1], frame_dims))

save_frame_changes(frames, "frame_changes.dat")
loaded_frames = load_frame_changes("frame_changes.dat")

print(loaded_frames)