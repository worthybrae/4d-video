import numpy
from scipy.sparse import coo_matrix

# Suppose you have points (i, j) with values, e.g., (row_index, col_index, value)
points = [(0, 1, 10), (2, 3, 20), (4, 5, 30)]  # (row, column, value)
height = 100
width = 100
depth = 100

# Split the points into rows, columns, and data
rows, cols, data = zip(*points)

# Create a sparse matrix
matrix = coo_matrix((data, (rows, cols)), shape=(height, width))


print(type(matrix))
