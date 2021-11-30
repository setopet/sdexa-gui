import numpy as np
from io import StringIO, BytesIO
from PIL import Image as PILImage
from backend import Image

standard_shape = (512, 512)
zeros = np.zeros(standard_shape)
ones = np.ones(standard_shape)


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
