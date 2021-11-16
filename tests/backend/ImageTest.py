import unittest
import numpy as np
from io import StringIO, BytesIO
from PIL import Image as PILImage
from backend import Image


class ImageTest(unittest.TestCase):
    def test_creation_from_text_file(self):
        array = [[0, 1], [1, 0]]
        file = get_txt_from_array(array, "test.csv")
        image = Image(file)
        self.assertTrue(np.array_equal(image.full_image, array))

    def test_creation_from_image(self):
        array = [[0, 202], [0, 202]]
        file = get_jpg_from_array(array, "test.jpg")
        image = Image(file)
        self.assertTrue(np.array_equal(image.full_image, array))

    def test_creation_from_npy(self):
        array = [[0, 1], [1, 0]]
        file = get_npy_from_array(array, "test.npy")
        image = Image(file)
        self.assertTrue(np.array_equal(image.full_image, array))

    def test_image_padding(self):
        array = [[0, 1], [1, 0]]
        file = get_txt_from_array(array)
        image = Image(file)
        self.assertEqual(image.image.shape, (512, 512))
        self.assertTrue(np.array_equal(image.image[0:2, 0:2], array))

    def test_image_cropping(self):
        array = np.ones((600, 600))
        file = get_txt_from_array(array)
        image = Image(file)
        self.assertEqual(image.image.shape, (512, 512))
        self.assertTrue(np.array_equal(image.image, array[0:512, 0:512]))

    def test_set_position(self):
        # TODO
        pass


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
