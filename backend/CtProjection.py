import numpy as np

from backend.helpers import save_timestamped_image, normalize_array_for_uint8


class CtProjection:
    def __init__(self, file):
        self.ct_projection = np.load(file)
        self.segmentation = None
        return

    def get_registration_result(self, output_path):
        return save_timestamped_image(output_path, self.overlay_images())

    def get_segmentation(self):
        if self.segmentation is not None:
            return self.segmentation
        mask_path = 'C:\\Users\\Sebastian\\LRZ Sync+Share\\Informatik\\Bachelorarbeit\\Daten\\CT_data\\mask\\AL.npy'
        self.segmentation = np.sum(np.load(mask_path), axis=1)
        return self.segmentation

    def overlay_images(self):
        result = normalize_array_for_uint8(np.sum(self.ct_projection, axis=1))
        result = np.stack([result, result, result])
        mask = self.get_segmentation()
        result[0] += mask * (100 / mask)
        result = normalize_array_for_uint8(result).astype('uint8')
        result = np.rot90(np.rot90(result.transpose(2, 1, 0)))
        x,y,_ = result.shape
        return np.pad(result, ((512-x, 0), (512-y, 0), (0,0)), 'constant')