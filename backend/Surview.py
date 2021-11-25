"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import numpy as np
from backend.sdexa import calculate_bone_density
from config import CONFIG
from backend import *


class Surview(Image):
    """Loads and manages the surview image as array."""
    def __init__(self, file, window=None):
        super().__init__(file, window)
        self.segmentation = None
        self.scatter = None
        self.soft_tissue_region = (0, 0, 50, 50)
        self.abmd_result = None

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
        scatter = get_array_from_file(file)
        if scatter.shape != self.full_image.shape:
            raise Exception(f"Scatter image shape {scatter.shape} "
                            f" is not identical to surview image shape {self.full_image.shape}!")
        self.scatter = scatter

    def delete_scatter(self):
        self.scatter = None

    def set_soft_tissue_region(self, region):
        x, y, dx, dy = region  # Frontend x and y axis can't be trusted
        self.soft_tissue_region = (x, y, dx, dy)

    def calculate_bone_density(self):
        if self.scatter is None:
            raise Exception("Bone density cannot be calculated without scatter image!")
        scatter = self.scatter
        x, y, dx, dy = self.region
        scatter = insert_padding(scatter[x:x+dx, y:y+dy])
        scatter = crop_image((x, y), scatter)
        self.abmd_result =\
            calculate_bone_density(self.image, self.get_segmentation(), scatter, self.soft_tissue_region)

    def get_bone_density_image(self):
        bone_density_matrix = self.abmd_result.bone_density_matrix
        image = np.where( bone_density_matrix > 0, bone_density_matrix, np.zeros(bone_density_matrix.shape))
        return to_normalized_red_uint8_rgb(image)
