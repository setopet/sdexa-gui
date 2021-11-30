from unittest import TestCase
from backend import Surview
from tests.helpers import *


class SegmentationTest(TestCase):
    def test_segmentation(self):
        file = get_txt_from_array(ones)
        image = Surview(file)
        segmentation = image.get_segmentation()
        self.assertEqual(segmentation.shape, standard_shape)
