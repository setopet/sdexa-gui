import numpy as np
from Config import CONFIG
from backend.segmentation.BaseModel import BaseModel
from torchvision.transforms import transforms


def perform_segmentation(image):
    # TODO: Only load this once for performance reasons
    model = BaseModel.load_from_checkpoint(CONFIG['CHECKPOINT_PATH'])
    model.float()  # necessary, because pytorch expects type 'double' otherwise
    tensor = model(transforms.ToTensor()(image)[None, ...])  # pytorch expects a batch of data, so a dimension is added
    array = tensor.detach().numpy().squeeze().astype(int)  # TODO: Conversion seems to generate negative numbers
    return np.where(array > 0, np.ones(array.shape), np.zeros(array.shape))
