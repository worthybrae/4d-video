import numpy as np


def get_random_rgba_bytes():
    random_rgba_values = np.random.randint(-128, 127, size=4, dtype=np.int16)
    bytes_list = [value.tobytes() for value in random_rgba_values]
    return b''.join(bytes_list)

def 

length = 1000
width = 1000
depth = 1000
density_rate = .05

total_cells = length * width * depth
dense_matrix = np.zeros((length, width, depth), dtype=np.int16)
populated_cells = int(total_cells * density_rate)

initial_view = {}
for _ in range(populated_cells):
    x, y, z = np.random.randint(0, 1000, size=3, dtype=np.int16)
    if x not in initial_view:
        initial_view[x] = {y: {z: get_random_rgba_bytes()}}
    elif y not in initial_view[x]:
        initial_view[x][y] = {z: get_random_rgba_bytes()}
    else:
        initial_view[x][y][z] = get_random_rgba_bytes()


    


