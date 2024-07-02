import numpy as np


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def mag(vector):
    return np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
