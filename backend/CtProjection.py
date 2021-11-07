import numpy as np


class CtProjection:
    def __init__(self, file):
        self.ct_projection = np.load(file)
        return

    def get_ct_projection(self):
        return self.ct_projection
