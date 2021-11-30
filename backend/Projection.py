"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import *


class Projection(Image):
    """Loads and manages the projection image as array."""
    def __init__(self, file, window=None):
        super().__init__(file, window)
        self.registration = None
        return

    def get_registration_overlay_image(self, image):
        if self.registration is None:
            return None
        return overlay_with_mask(image, self.registration, 50, self.window)

    def get_registration_result_csv(self):
        if self.registration is None:
            return None
        return image_to_csv(self.registration, format_string="%i")

    def register_on_image(self, image, number_iterations=10000):
        self.registration = create_mask(perform_registration(
            to_uint8(normalize_array(image)),
            to_uint8(normalize_array(self.image)),
            number_iterations), 20)

    def delete_registration(self):
        self.registration = None
