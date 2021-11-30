import math
from unittest import TestCase
from backend import Surview
from tests.helpers import *


class SdexaTest(TestCase):
    def test_calculation(self):
        image = Surview(get_txt_from_array(ones))
        image.set_scatter(get_txt_from_array(zeros))
        image.segmentation = zeros
        image.calculate_bone_density()
        result = image.abmd_result
        self.assertEqual(result.bone_density_matrix.shape, standard_shape)
        self.assertFalse(math.isnan(result.bone_density_mean))
        self.assertFalse(math.isnan(result.bone_density_std))
