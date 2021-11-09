import numpy as np
from backend.segmentation.BaseModel import BaseModel
from torchvision.transforms import transforms


saved_models = {}


def perform_segmentation(image, checkpoint_path):
    if saved_models.get(checkpoint_path) is None:
        saved_models[checkpoint_path] = BaseModel.load_from_checkpoint(checkpoint_path)
    model = saved_models.get(checkpoint_path)
    model.float()  # necessary, because pytorch expects type 'double' otherwise
    tensor = model(transforms.ToTensor()(image)[None, ...])  # pytorch expects a batch of data, so a dimension is added
    array = tensor.detach().numpy().squeeze().astype(int)  # TODO: Conversion seems to generate negative numbers
    return np.where(array > 0, np.ones(array.shape), np.zeros(array.shape))
