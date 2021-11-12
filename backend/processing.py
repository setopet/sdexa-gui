import os
import numpy as np
from io import StringIO
from PIL import Image
from numpy import asarray


def to_uint8(image):
    return image.astype('uint8')


def to_normalized_uint8(image):
    return to_uint8(normalize_array_for_uint8(image))


def to_rgb(image):
    return np.stack([image, image, image]).transpose((1, 2, 0))


def to_normalized_rgb(image, window=None):
    image = set_window(image, window)
    image = normalize_array_for_uint8(image)
    return to_rgb(image)

# Reproduzieren: Window 0,2000 setzen, ohne das Rechteck zu verschieben
# Dann Recht eck ganz oben setzen
# dann OK -> im Backend kommt Position -1 an

def to_normalized_uint8_rgb(image, window=None):
    return to_uint8(to_normalized_rgb(image, window))


def normalize_array_for_uint8(image):
    result = image - image.min()
    return result * (255 / result.max())


def set_window(image, window):
    if window is None:
        return image
    minimum, maximum = window
    if minimum is not None:
        image = np.where(image >= minimum, image, np.zeros(image.shape))
    if maximum is not None:
        image = np.where(image <= maximum, image, np.zeros(image.shape))
    return image


def create_mask(image, threshold=0):
    array = np.where(image >= threshold, image, np.zeros(image.shape))
    return to_uint8(np.where(array == 0, array, np.ones(array.shape)))


def overlay_with_mask(image, mask, mask_intensity=50, window=None):
    image = to_normalized_rgb(image, window)
    image[:, :, 0] += mask * mask_intensity
    return to_uint8(image)


# TODO: ".nii"
def get_array_from_file(file):
    _, extension = os.path.splitext(file.filename)
    if extension == ".txt":
        array = np.loadtxt(file, delimiter=",")
    elif extension == ".csv":
        array = np.loadtxt(file, delimiter=",")
    elif extension == ".npy":
        array = np.load(file)
    elif extension == ".jpg" or extension == ".jpeg" or extension == ".png":
        image = Image.open(file)
        array = asarray(image)
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
    stream = StringIO()
    if format_string is not None:
        np.savetxt(stream, image, fmt=format_string, delimiter=",")
    else:
        np.savetxt(stream, image, delimiter=",")
    return stream.getvalue()


def insert_padding(image, new_size=512):
    shape_x, shape_y = image.shape
    if shape_x < new_size:
        image = np.pad(image, ((0, new_size - shape_x), (0, 0)), 'constant')
    if shape_y < new_size:
        image = np.pad(image, ((0, 0), (0, new_size-shape_y)), 'constant')
    return image


def crop_image(position, image, new_size=512):
    shape_x, shape_y = image.shape
    y, x = position  # Frontend x and y axis can't be trusted
    # If one of the values is out of bound get the value which is the maximum value possible
    if x+new_size >= shape_x:
        x = shape_x - new_size
    if y+new_size >= shape_y:
        y = shape_y - new_size
    return image[x:x + new_size, y:y + new_size]
