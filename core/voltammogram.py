import numpy as np

class Voltammogram:
    def __init__(self, potential, current):
        self.potential = np.asarray(potential)
        self.current = np.asarray(current)
