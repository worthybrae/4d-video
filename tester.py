import numpy as np


total_pixels = 1000

rgba = np.random.randint(0, high=256, size=(total_pixels, 4), dtype=np.uint8)

# Convert and shift each component, then combine
rgba_uint32 = (rgba[:, 0].astype(np.uint32) << 24) | \
                (rgba[:, 1].astype(np.uint32) << 16) | \
                (rgba[:, 2].astype(np.uint32) << 8) | \
                (rgba[:, 3].astype(np.uint32))

print(rgba_uint32, type(rgba_uint32))