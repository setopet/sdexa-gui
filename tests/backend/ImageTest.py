import unittest
import numpy as np
from io import StringIO, BytesIO
from PIL import Image as PILImage
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
        array = [[0, 1], [1, 0]]
        image = get_image_from_array(array)
        self.assertTrue(np.array_equal(image.image[0:2, 0:2], array))

    def test_crops_image(self):
        array = np.ones((600, 600))
        image = get_image_from_array(array)
        self.assertTrue(np.array_equal(image.image, array[0:512, 0:512]))

    def test_sets_position_x(self):
        array = np.pad(np.ones((513, 1)), ((0, 0), (0, 512)), 'constant')
        image = get_image_from_array(array)
        image.set_image_position((1, 0))
        self.assertTrue(np.array_equal(image.image, np.zeros((512, 512))))

    def test_sets_position_y(self):
        array = np.pad(np.ones((1, 513)), ((0, 512), (0, 0)), 'constant')
        image = get_image_from_array(array)
        image.set_image_position((0, 1))
        self.assertTrue(np.array_equal(image.image, np.zeros((512, 512))))

    def test_sets_position_negative(self):
        array = np.ones((513, 513))
        image = get_image_from_array(array)
        image.set_image_position((-1, -1))
        self.assertTrue(np.array_equal(image.image, np.ones((512, 512))))

    def test_sets_position_out_of_bound(self):
        array = np.ones((512, 512))
        image = get_image_from_array(array)
        image.set_image_position((42, 42))
        self.assertTrue(np.array_equal(image.image, np.ones((512, 512))))

    def test_returns_jpg_convertible_image(self):
        array = np.ones((512, 512))
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
        array = np.ones((512, 512)) * 42
        image = get_image_from_array(array)
        image.set_window((0, 41))
        self.assertTrue(np.array_equal(image.get_image(), np.zeros((512, 512, 3))))

    def test_sets_window_min(self):
        array = np.ones((512, 512)) * -1
        image = get_image_from_array(array)
        image.set_window((0, 0))
        self.assertTrue(np.array_equal(image.get_image(), np.zeros((512, 512, 3))))

    def test_returns_image_csv(self):
        array = np.ones((512, 512))
        image = get_image_from_array(array)
        csv = image.get_image_csv()
        stream = BytesIO(csv.encode())
        self.assertTrue(np.array_equal(np.loadtxt(stream, delimiter=","), array))


def get_image_from_array(array):
    return Image(get_txt_from_array(array))


def get_txt_from_array(array, filename="test.txt"):
    file = StringIO()
    np.savetxt(file, np.asarray(array), delimiter=",")
    file.seek(0)
    file.filename = filename
    return file


def get_jpg_from_array(array, filename):
    file = BytesIO()
    rgb_image = np.stack([array, array, array]).transpose((1, 2, 0)).astype('uint8')
    PILImage.fromarray(rgb_image).save(file, format='JPEG')
    file.seek(0)
    file.filename = filename
    return file


def get_npy_from_array(array, filename):
    file = BytesIO()
    np.save(file, np.asarray(array))
    file.seek(0)
    file.filename = filename
    return file
