import numpy as np
from helpers import save_timestamped_image, to_uint8, to_normalized_rgb
from segmentation.Segmentation import perform_segmentation


class Surview:
    def __init__(self, file, cropping=(0, 0)):
        x, y = cropping
        array = np.loadtxt(file, delimiter=",")[x:x + 512, y:y + 512]
        self.surview = array
        self.segmentation = None

    def get_surview_image(self, output_path):
        return save_timestamped_image(output_path, self.surview)

    def get_segmentation_image(self, output_path):
        return save_timestamped_image(output_path, self.segmentation)

    def get_segmentation_overlay_image(self, output_path):
        return save_timestamped_image(output_path, self.overlay_images())

    def get_segmentation(self):
        if self.segmentation is None:
            self.segmentation = perform_segmentation(self.surview)
        return self.segmentation

    def overlay_images(self, mask_intensity=50):
        image = to_normalized_rgb(self.surview, (0, 2000))
        image[:, :, 0] += self.get_segmentation() * mask_intensity
        return np.rot90(to_uint8(image))


