from segmentation.BaseModel import BaseModel
from torchvision.transforms import transforms

checkpoint_path = './segmentation/checkpoints/0912_194939.ckpt'


def perform_segmentation(image):
    model = BaseModel.load_from_checkpoint(checkpoint_path)
    model.float()  # necessary, because pytorch expects type 'double' otherwise
    tensor = model(transforms.ToTensor()(image)[None, ...])  # pytorch expects a batch of data, so a dimension is added
    array = tensor.detach().numpy().squeeze().astype(int)
    return array > 0  # conversion seems to generate negative numbers
