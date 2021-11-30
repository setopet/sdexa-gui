"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import os as _os
import numpy as _np
from io import StringIO as _StringIO
from PIL import Image as _Image


def to_uint8(image):
    return image.astype('uint8')


def to_normalized_image(image, window):
    image = set_window(image, window)
    return normalize_array(image, 255)


def to_rgb(image):
    return _np.stack([image, image, image]).transpose((1, 2, 0))


def to_red_rgb(image):
    return _np.stack([image, _np.zeros(image.shape), _np.zeros(image.shape)]).transpose((1, 2, 0))


def to_normalized_rgb(image, window):
    image = to_normalized_image(image, window)
    return to_rgb(image)


def to_normalized_uint8_rgb(image, window=None):
    return to_uint8(to_normalized_rgb(image, window))


def normalize_array(image, max_value=255):
    result = image - image.min()
    maximum = result.max()
    if maximum == 0:
        return result
    return result * (max_value / result.max())


def set_window(image, window):
    if window is None:
        return image
    minimum, maximum = window
    if minimum is not None:
        image = _np.where(image >= minimum, image, _np.zeros(image.shape))
    if maximum is not None:
        image = _np.where(image <= maximum, image, _np.zeros(image.shape))
    return image


def create_mask(image, threshold=0):
    array = _np.where(image >= threshold, image, _np.zeros(image.shape))
    return to_uint8(_np.where(array == 0, array, _np.ones(array.shape)))


def overlay_with_mask(image, mask, mask_intensity=50, window=None):
    image = to_normalized_rgb(image, window)
    image[:, :, 0] += mask * mask_intensity
    return to_uint8(image)


# TODO: ".nii"
def get_array_from_file(file):
    _, extension = _os.path.splitext(file.filename)
    if extension == ".txt":
        array = _np.loadtxt(file, delimiter=",")
    elif extension == ".csv":
        array = _np.loadtxt(file, delimiter=",")
    elif extension == ".npy":
        array = _np.load(file)
    elif extension == ".jpg" or extension == ".jpeg" or extension == ".png":
        image = _Image.open(file)
        array = _np.asarray(image)
        if array.ndim == 3:
            array = array[:, :, 0]
    else:
        raise Exception("Invalid file type! Supported file types: .jpg, .png, .npy, .csv, .txt")
    dimensions = array.ndim
    array = array.squeeze()
    if array.ndim != 2:
        raise Exception("Input has a wrong number of dimensions (" + str(dimensions) + "). It should have 2!")
    return array


def image_to_csv(image, format_string=None):
    stream = _StringIO()
    if format_string is not None:
        _np.savetxt(stream, image, fmt=format_string, delimiter=",")
    else:
        _np.savetxt(stream, image, delimiter=",")
    return stream.getvalue()


def insert_padding(image, new_size=512):
    shape_x, shape_y = image.shape
    if shape_x < new_size:
        pad_left = (new_size - shape_x)//2
        image = _np.pad(image, ((pad_left, new_size - (shape_x + pad_left)), (0, 0)), 'constant', constant_values=1)
    if shape_y < new_size:
        pad_down = (new_size - shape_y)//2
        image = _np.pad(image, ((0, 0), (pad_down, new_size - (shape_y + pad_down))), 'constant', constant_values=1)
    return image


def crop_image(position, image, new_size=512):
    shape_x, shape_y = image.shape
    x, y = position
    # If one of the values is out of bound get the value which is the maximum value possible
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x+new_size > shape_x:
        x = shape_x - new_size
    if y+new_size > shape_y:
        y = shape_y - new_size
    return image[x:x + new_size, y:y + new_size]
