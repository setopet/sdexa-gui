import numpy as np
from helpers import set_window, save_image


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
    result[:, :, 0] += mask.squeeze() * 100  # multiplying mask with value between 1 and 255 for better displaying
    return result.astype('uint8')


# will be removed for real segmentation (Burak's code)
# mask contains only ones and zeros.
def get_segmentation(image):
    mask_path = 'C:\\Users\\Sebastian\\LRZ Sync+Share\\Informatik\\Bachelorarbeit\\Daten\\Surview_data\\' \
                'S002768_S1000_output-photo_r1_mask.npy'
    return np.load(mask_path)
