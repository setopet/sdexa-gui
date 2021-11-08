import numpy as np

from backend.processing import create_mask, to_normalized_rgb, to_normalized_uint8


class CtProjection:
    def __init__(self, file):
        self.ct_projection = np.load(file)
        return

    def get_ct_projection(self):
        return self.ct_projection

    @staticmethod
    def overlay_registration(surview, registration_result):
        mask = create_mask(registration_result, 15)
        image = to_normalized_rgb(surview)
        image[:, :, 0] += mask * 50
        return to_normalized_uint8(image)
