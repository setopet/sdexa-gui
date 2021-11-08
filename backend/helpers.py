from io import StringIO
import numpy as np


def to_uint8(image):
    return image.astype('uint8')


def to_normalized_uint8(image):
    return to_uint8(normalize_array_for_uint8(image))


def to_rgb(image):
    return np.stack([image, image, image]).transpose(1, 2, 0)


def to_normalized_rgb(image, window=None):
    if window is not None:
        minimum, maximum = window
        image = set_window(image, minimum, maximum)
    image = normalize_array_for_uint8(image)
    return to_rgb(image)


def to_normalized_uint8_rgb(image, window=None):
    return to_uint8(to_normalized_rgb(image, window))


def normalize_array_for_uint8(image):
    result = image - image.min()
    return result * (255 / result.max())


def set_window(image, minimum, maximum):
    image = np.where(image >= minimum, image, np.zeros(image.shape))
    return np.where(image <= maximum, image, np.zeros(image.shape))


def image_to_csv(image, format_string=None):
    stream = StringIO()
    if format_string is not None:
        np.savetxt(stream, image, fmt=format_string, delimiter=",")
    else:
        np.savetxt(stream, image, delimiter=",")
    return stream.getvalue()
