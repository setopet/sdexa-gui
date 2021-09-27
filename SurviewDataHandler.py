import numpy as np
from torchvision.transforms import transforms
from helpers import set_window, save_image
from segmentation.base import BaseModel


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
    result[:, 0:512, 0] += (mask > 0).squeeze() * 100  # multiplying mask with value between 1 and 255 for better displaying
    return result.astype('uint8')


# will be removed for real segmentation (Burak's code)
# mask contains only ones and zeros.
def get_segmentation(image):
    model = BaseModel.load_from_checkpoint('./segmentation/checkpoints/0912_194939.ckpt')
    i = image[0,0:512,0:512]
    model.float()
    # Pytorch erwartet Batch als Eingabe, das [None, ...] fügt eine "Batch"-Dimension hinzu
    result = model(transforms.ToTensor()(i)[None, ...])
    return result.detach().numpy().squeeze().astype(int)
