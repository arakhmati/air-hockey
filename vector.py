import numpy as np

magnitude = np.linalg.norm
def normalize(array):
    mag = magnitude(array)
    if mag != 0.0:
        array /= mag
    return array