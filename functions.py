import numpy as np


def unit_vector(vector):
    if mag(vector) != 0:
        return vector / np.linalg.norm(vector)
    else:
        return np.zeros(3)


def mag(vector):
    # return np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    return np.linalg.norm(vector)
