import numpy as np
from backend.helpers import to_uint8, to_normalized_rgb, to_normalized_uint8_rgb, image_to_csv
from backend.segmentation.Segmentation import perform_segmentation


class Surview:
    def __init__(self, file, cropping=(0, 0), window=None):
        self.full_image = np.loadtxt(file, delimiter=",")
        self.cropped_image = None
        self.set_cropping(cropping)
        self.window = window
        self.segmentation = None

    def set_cropping(self, cropping):
        y, x = cropping
        shape_x, shape_y = self.full_image.shape
        if x+512 >= shape_x:
            x = 0
        if y+512 >= shape_y:
            y = 0
        self.cropped_image = self.full_image[x:x + 512, y:y + 512]

    def get_image(self):
        return to_normalized_uint8_rgb(self.cropped_image, self.window)

    def get_full_image(self):
        return to_normalized_uint8_rgb(self.full_image, self.window)

    def get_segmentation_overlay_image(self):
        return self.overlay_images()

    def get_segmentation_csv(self):
        return image_to_csv(to_uint8(self.get_segmentation()), format_string="%i")

    def get_image_csv(self):
        return image_to_csv(self.cropped_image)

    def get_segmentation(self):
        if self.segmentation is None:
            self.segmentation = perform_segmentation(self.cropped_image)
        return self.segmentation

    def overlay_images(self, mask_intensity=50):
        image = to_normalized_rgb(self.cropped_image, self.window)
        image[:, :, 0] += self.get_segmentation() * mask_intensity
        return to_uint8(image)
