"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import unittest
from tests.helpers import *
from backend import Image


class ImageTest(unittest.TestCase):
    def test_creates_from_text_file(self):
        array = [[0, 1], [1, 0]]
        file = get_txt_from_array(array, "test.csv")
        image = Image(file)
        self.assertTrue(np.array_equal(image.full_image, array))

    def test_creates_from_image(self):
        array = [[0, 202], [0, 202]]
        file = get_jpg_from_array(array, "test.jpg")
        image = Image(file)
        self.assertTrue(np.array_equal(image.full_image, array))

    def test_creates_from_npy(self):
        array = [[0, 1], [1, 0]]
        file = get_npy_from_array(array, "test.npy")
        image = Image(file)
        self.assertTrue(np.array_equal(image.full_image, array))

    def test_pads_image(self):
        array = zeros
        image = get_image_from_array(array)
        image.set_image_region((255, 255, 2, 2))
        self.assertEqual(image.image.shape, standard_shape)

    def test_crops_image(self):
        array = np.ones((600, 600))
        image = get_image_from_array(array)
        self.assertTrue(np.array_equal(image.image, array[0:512, 0:512]))

    def test_sets_position_x(self):
        array = np.pad(np.ones((513, 1)), ((0, 0), (0, 512)), 'constant')
        image = get_image_from_array(array)
        image.set_image_region((1, 0, 512, 512))
        self.assertTrue(np.array_equal(image.image, zeros))

    def test_sets_position_y(self):
        array = np.pad(np.ones((1, 513)), ((0, 512), (0, 0)), 'constant')
        image = get_image_from_array(array)
        image.set_image_region((0, 1, 512, 512))
        self.assertTrue(np.array_equal(image.image, np.zeros((512, 512))))

    def test_sets_region(self):
        array = np.pad(ones, ((512, 0), (512, 0)), 'constant')
        image = get_image_from_array(array)
        image.set_image_region((512, 512, 512, 512))
        self.assertTrue(np.array_equal(image.image, ones))

    def test_sets_position_negative(self):
        array = np.ones((513, 513))
        image = get_image_from_array(array)
        image.set_image_region((-1, -1, 512, 512))
        self.assertTrue(np.array_equal(image.image, ones))

    def test_sets_position_out_of_bound(self):
        array = ones
        image = get_image_from_array(array)
        image.set_image_region((42, 42, 512, 512))
        self.assertEqual(image.image.shape, (512, 512))

    def test_returns_jpg_convertible_image(self):
        array = ones
        image = get_image_from_array(array)
        result = image.get_image()
        self.assertEqual(result.shape, (512, 512, 3))
        self.assertEqual(result.dtype, 'uint8')

    def test_returns_jpg_convertible_full_image(self):
        array = np.ones((513, 513))
        image = get_image_from_array(array)
        result = image.get_full_image()
        self.assertEqual(result.shape, (513, 513, 3))
        self.assertEqual(result.dtype, 'uint8')

    def test_sets_window_max(self):
        array = ones * 42
        image = get_image_from_array(array)
        image.set_window((0, 41))
        self.assertTrue(np.array_equal(image.get_image(), np.zeros((512, 512, 3))))

    def test_sets_window_min(self):
        array = ones * -1
        image = get_image_from_array(array)
        image.set_window((0, 0))
        self.assertTrue(np.array_equal(image.get_image(), np.zeros((512, 512, 3))))

    def test_returns_image_csv(self):
        array = ones
        image = get_image_from_array(array)
        csv = image.get_image_csv()
        stream = BytesIO(csv.encode())
        self.assertTrue(np.array_equal(np.loadtxt(stream, delimiter=","), array))

