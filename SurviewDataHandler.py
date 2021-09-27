import numpy as np
from helpers import set_window, save_image
from segmentation.Segmentation import perform_segmentation


class SurviewDataHandler:
    def __init__(self, directory):
        self.directory = directory

    def process_and_save_image(self, file):
        image = set_window(np.load(file))
        mask = get_segmentation(image)
        return save_image(self.directory, overlay_images(image, mask))


# overlay image with mask
def overlay_images(image, mask):
    result = np.stack([image, image, image]).transpose(2, 3, 0, 1).squeeze()
    result[:, 0:512, 0] += mask * 100  # multiplying mask with value between 1 and 255 for better displaying
    return result.astype('uint8')


def get_segmentation(image):
    return perform_segmentation(image[0, 0:512, 0:512])

