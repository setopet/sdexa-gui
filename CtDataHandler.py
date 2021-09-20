import numpy as np
from helpers import set_window, save_image


class CtDataHandler:
    def __init__(self, directory):
        self.directory = directory

    def process_and_save_image(self, file):
        image = np.load(file)
        mask = get_segmentation(image)
        overlay_image = overlay_images(image, mask)
        return save_image(self.directory, overlay_image)


# will be removed for real segmentation (Deep Spine)
def get_segmentation(image):
    mask_path = 'C:\\Users\\Sebastian\\LRZ Sync+Share\\Informatik\\Bachelorarbeit\\Daten\\CT_data\\mask\\AL.npy'
    mask = np.sum(np.load(mask_path), axis=1)
    return mask


# overlay image with mask
def overlay_images(image, mask):
    result = set_window(np.sum(image, axis=1))
    result = np.stack([result, result, result])
    result[0] += mask * (100 / mask.max())
    result = set_window(result).astype('uint8')
    return result.transpose(2, 1, 0)
