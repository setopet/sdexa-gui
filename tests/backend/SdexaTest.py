from unittest import TestCase
from backend import Surview
from tests.backend.helpers import *


class SdexaTest(TestCase):
    def test_calculation(self):
        image = Surview(get_txt_from_array(ones))
        image.set_scatter(get_txt_from_array(zeros))
        image.segmentation = zeros
        image.calculate_bone_density()
        result = image.abmd_result.bone_density_matrix
        self.assertEqual(result.shape, standard_shape)