import os

import numpy as np
from datetime import datetime
from PIL import Image


def to_uint8(image):
    return image.astype('uint8')


def to_normalized_uint8(image):
    return to_uint8(normalize_array_for_uint8(image))


def to_rgb(image):
    image = np.stack([image, image, image]).transpose(1, 2, 0)
    return image


def to_normalized_rgb(image, window=None):
    if window is not None:
        minimum, maximum = window
        image = set_window(image, minimum, maximum)
    image = normalize_array_for_uint8(image)
    return to_rgb(image)


def normalize_array_for_uint8(image):
    result = image - image.min()
    return result * (255 / result.max())


def set_window(image, minimum, maximum):
    image = np.where(image >= minimum, image, np.zeros(image.shape))
    image = np.where(image <= maximum, image, np.zeros(image.shape))
    return image


def save_timestamped_image(path, image):
    filename = datetime.now().strftime("%y%m%d%H%M%S")
    path = os.path.join(path, filename + '.jpeg')
    Image.fromarray(image).save(path)
    return filename + '.jpeg'
