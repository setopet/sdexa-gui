import numpy as np

from backend.helpers import to_uint8, to_normalized_rgb, to_normalized_uint8_rgb, image_to_csv, get_array_from_file
from backend.segmentation.Segmentation import perform_segmentation


class Surview:
    def __init__(self, file, window=None):
        self.full_image = get_array_from_file(file).squeeze()
        self.image = None
        self.window = window
        self.segmentation = None

    def set_image_position(self, positions):
        image = self.insert_padding()
        self.crop_image(positions, image)

    def crop_image(self, positions, image):
        shape_x, shape_y = image.shape
        y, x = positions  # Frontend x and y axis can't be trusted
        # If one of the values is out of bound get the value which is the maximum value possible
        if x+512 >= shape_x:
            x = shape_x - 512
        if y+512 >= shape_y:
            y = shape_y - 512
        self.image = image[x:x + 512, y:y + 512]

    def insert_padding(self):
        shape_x, shape_y = self.full_image.shape
        image = self.full_image
        if shape_x < 512:
            image = np.pad(image, ((512 - shape_x, 0), (0, 0)), 'constant')
        if shape_y < 512:
            image = np.pad(image, ((0,0), (512-shape_y, 0)), 'constant')
        return image

    def get_image(self):
        return to_normalized_uint8_rgb(self.image, self.window)

    def get_full_image(self):
        return to_normalized_uint8_rgb(self.full_image, self.window)

    def get_segmentation_overlay_image(self):
        return self.overlay_images()

    def get_segmentation_csv(self):
        return image_to_csv(to_uint8(self.get_segmentation()), format_string="%i")

    def get_image_csv(self):
        return image_to_csv(self.image)

    def get_segmentation(self):
        if self.segmentation is None:
            self.segmentation = perform_segmentation(self.image)
        return self.segmentation

    def overlay_images(self, mask_intensity=50):
        image = to_normalized_rgb(self.image, self.window)
        image[:, :, 0] += self.get_segmentation() * mask_intensity
        return to_uint8(image)
