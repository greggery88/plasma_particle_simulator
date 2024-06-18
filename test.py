import numpy as np


a_x = np.array([1, 0, 0])
a_y = np.array([0, 1, 0])
a_z = np.array([0, 0, 0])

a_n = np.cross(a_x, a_y)

print(a_n)
