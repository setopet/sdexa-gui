from backend.sdexa import calculate_bone_density
from config import CONFIG
from backend import *


class Surview(Image):
    """Loads and manages the surview image as array."""
    def __init__(self, file, window=None):
        super().__init__(file, window)
        self.segmentation = None
        self.scatter = None

    def get_surview_array(self):
        return self.image

    def get_segmentation(self):
        if self.segmentation is None:
            self.segmentation = perform_segmentation(self.image, CONFIG['CHECKPOINT_PATH'])
        return self.segmentation

    def get_segmentation_overlay_image(self):
        return overlay_with_mask(self.image, self.get_segmentation(), 50, self.window)

    def get_segmentation_csv(self):
        return image_to_csv(to_uint8(self.get_segmentation()), format_string="%i")

    def set_scatter(self, file):
        self.scatter = get_array_from_file(file)

    def calculate_bone_density(self):
        if self.scatter is None:
            raise Exception("Bone densitiy cannot be calculated without scatter image!")
        return calculate_bone_density()
