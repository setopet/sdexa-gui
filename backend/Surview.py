"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import numpy as np
from config import CONFIG
from backend.sdexa import calculate_bone_density
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

    def set_custom_segmentation(self, file):
        custom_segmentation = create_mask(get_array_from_file(file))
        if custom_segmentation.shape == (512, 512):
            self.segmentation = custom_segmentation
        elif custom_segmentation.shape == self.full_image.shape:
            self.segmentation = pad_and_crop_image(custom_segmentation, self.region)

    def get_segmentation_overlay_image(self):
        return overlay_with_mask(self.image, self.get_segmentation(), 50, self.window)

    def get_segmentation_csv(self):
        return image_to_csv(to_uint8(self.get_segmentation()), format_string="%i")

    def set_scatter(self, file):
        scatter = get_array_from_file(file)
        if scatter.shape != self.full_image.shape:
            raise Exception(f"Scatter image shape {scatter.shape} "
                            f" is not identical to surview image shape {self.full_image.shape}!")
        self.scatter = pad_and_crop_image(scatter, self.region)

    def delete_scatter(self):
        self.scatter = None

    def set_soft_tissue_region(self, region):
        x, y, dx, dy = self.get_corrected_region(region)
        shape_x, shape_y = self.image.shape
        if x + dx > shape_x:
            dx = shape_x - x
        if y + dy > shape_y:
            dy = shape_y - x
        self.soft_tissue_region = x, y, dx, dy

    def calculate_bone_density(self):
        if self.scatter is None:
            raise Exception("Bone density cannot be calculated without scatter image!")
        self.abmd_result =\
            calculate_bone_density(self.image, self.get_segmentation(), self.scatter, self.soft_tissue_region)

    def get_bone_density_image(self):
        if self.abmd_result is None:
            return None
        bone_density_matrix = self.abmd_result.bone_density_matrix
        image = np.where( bone_density_matrix > 0, bone_density_matrix, np.zeros(bone_density_matrix.shape))
        return to_normalized_uint8_rgb(image)

    def get_bone_density_mean(self):
        if self.abmd_result is None:
            return None
        return self.abmd_result.bone_density_mean

    def get_bone_density_std(self):
        if self.abmd_result is None:
            return None
        return self.abmd_result.bone_density_std

    def get_bone_density_image_csv(self):
        if self.abmd_result is None:
            return None
        return image_to_csv(self.abmd_result.bone_density_matrix)
