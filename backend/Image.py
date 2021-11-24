"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import *


class Image:
    """Loads and manages the image as array."""
    def __init__(self, file, window=None):
        self.full_image = get_array_from_file(file)
        self.position = (0, 0)
        self.image = self.set_image_position(self.position)
        self.window = window

    def set_image_position(self, position):
        """Set the position on the full image for the selected section."""
        self.position = position
        image = insert_padding(self.full_image)
        self.image = crop_image(position, image)
        return self.image

    def set_window(self, window):
        """Set the window of the image."""
        self.window = window

    def get_image(self):
        """Get the section of the image selected by the user."""
        return to_normalized_uint8_rgb(self.image, self.window)

    def get_full_image(self):
        """Get the full image."""
        return to_normalized_uint8_rgb(self.full_image, self.window)

    def get_image_csv(self):
        """Get the section of the image as csv."""
        return image_to_csv(self.image)
