"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import numpy as np
from backend.segmentation.BaseModel import BaseModel
from torchvision.transforms import transforms


saved_models = {}


def perform_segmentation(image, model_checkpoint_path):
    """Uses the pretrained pytorch model for segmentation of the image.
    :returns an array of zeros and ones, where the ones indicate segments
    """
    if saved_models.get(model_checkpoint_path) is None:
        saved_models[model_checkpoint_path] = BaseModel.load_from_checkpoint(model_checkpoint_path)
    model = saved_models.get(model_checkpoint_path)
    model.float()
    input_tensor = transforms.ToTensor()(image)[None, ...]  # pytorch expects a batch of data
    output_tensor = model.forward(input_tensor)
    result = output_tensor.detach().numpy().squeeze().astype(int)
    return np.where(result > 0, np.ones(result.shape), np.zeros(result.shape))
