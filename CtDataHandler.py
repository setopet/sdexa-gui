import numpy as np
from helpers import normalize_array_for_uint8, save_timestamped_image


class CtDataHandler:
    def __init__(self, directory):
        self.directory = directory

    def process_and_save_image(self, file):
        image = np.load(file)
        mask = get_segmentation(image)
        overlay_image = overlay_images(image, mask)
        return save_timestamped_image(self.directory, overlay_image)


# will be removed for real segmentation (Deep Spine)
def get_segmentation(image):
    mask_path = 'C:\\Users\\Sebastian\\LRZ Sync+Share\\Informatik\\Bachelorarbeit\\Daten\\CT_data\\mask\\AL.npy'
    mask = np.sum(np.load(mask_path), axis=1)
    return mask


# overlay image with mask
def overlay_images(image, mask):
    result = normalize_array_for_uint8(np.sum(image, axis=1))
    result = np.stack([result, result, result])
    result[0] += mask * (100 / mask.max())
    result = normalize_array_for_uint8(result).astype('uint8')
    result = np.rot90(np.rot90(result.transpose(2, 1, 0)))
    x,y,_ = result.shape
    return np.pad(result, ((512-x, 0), (512-y, 0), (0,0)), 'constant')