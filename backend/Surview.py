import numpy as np
from backend.helpers import to_uint8, to_normalized_rgb, to_normalized_uint8_rgb, image_to_csv
from backend.segmentation.Segmentation import perform_segmentation


class Surview:
    def __init__(self, file, cropping=(0, 0), window=None):
        self.full_image = np.loadtxt(file, delimiter=",")
        x, y = cropping
        self.cropped_image = self.full_image[x:x + 512, y:y + 512]
        self.window = window
        self.segmentation = None

    def get_image(self):
        return to_normalized_uint8_rgb(self.cropped_image, self.window)

    def get_segmentation_overlay_image(self):
        return self.overlay_images()

    def get_segmentation_csv(self):
        return image_to_csv(self.get_segmentation(), format_string="%i")

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
