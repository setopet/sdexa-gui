import cv2
import numpy as np

from os import listdir
from glob import glob


MAIN_DIR = "G:\\Code\\ba\\thesis-gui\\segmentation\\"
MASKS_DIR = 'images\\'
IMGS_DIR = 'images\\'
SAVE_DIR = 'G:\\Code\\ba\\thesis-gui\\segmentation\\'


#setzt Bereiche im Bild die kleiner als 300 sind auf 300, analog welche die größer 1300 auf 1300
def _window_image(image, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max

    return window_image


def _normalize_and_rescale(image):
    return (image / image.max()) * 255


def _reverse_axes(image):
    return np.transpose(image, tuple(reversed(range(image.ndim))))


def _crop_image(image, new_height=512, new_width=512):
    height, width = image.shape

    y0 = (height - new_height) // 2 if height >= new_height else 0
    x0 = (width - new_width) // 2 if width >= new_width else 0

    return image[y0:y0+new_height, x0:x0+new_width]


def _crop(image, center):
    height, width = image.shape
    diff = width - center
    if center <= 255:
        x, y = 0, 512
    elif diff < 255:
        x, y = width - 512, width
    else:
        x, y = center - 256, center + 256

    return image[0:512, x:y]


def _add_pad(image, new_height=512, new_width=512):
    height, width = image.shape

    final_image = np.zeros((new_height, new_width))

    pad_left = int((new_width - width) / 2)
    pad_top = int((new_height - height) / 2)

    # Replace the pixels with the image's pixels
    final_image[pad_top:pad_top + height, pad_left:pad_left + width] = image

    return final_image


# bestimmt glaub ich das oberste und unterste Pixel der Maske, das gesetzt ist
def _find_min_max_vertabrae(array):
    mask = np.argwhere(array.squeeze() == 1.0)
    min = mask[0][1]
    max = mask[-1][1]
    return min, max


# Ich glaube mit der Maske kann man z.B. 512x1024 Bild nehmen und in bestimmten Bereich z.B. 512x512 Rechteck diese auf 1 setzen, und nur dort wird segmentiert?
# Diese Maske kommt wohl nur zum Einsatz wenn W>512
if __name__ == '__main__':
    files = [file.split('.')[0] for file in listdir(MAIN_DIR + IMGS_DIR) if file.endswith('.npy')]

    for file in files:
        mask_file = glob(MAIN_DIR + MASKS_DIR + file + '*_r2.npy') or glob(MAIN_DIR + MASKS_DIR + file + '*_r1.npy')
        if not mask_file:
            continue

        img_file = glob(MAIN_DIR + IMGS_DIR + file + '*.npy')
        mask_array = np.load(mask_file[0]).squeeze()
        img_array = np.load(img_file[0]).squeeze()

        _, W = mask_array.shape
        if W > 512:
            min, max = _find_min_max_vertabrae(mask_array)

            mask_center = (min + max) // 2
            mask_array = _crop(mask_array, mask_center)
            img_array = _crop(img_array, mask_center)

        data = _window_image(img_array, 800, 1000)

        data = _normalize_and_rescale(data)

        cv2.imwrite(SAVE_DIR + MASKS_DIR + file + '_r0.png', mask_array * 255.0)
        cv2.imwrite(SAVE_DIR + IMGS_DIR + file + '.png', data)
