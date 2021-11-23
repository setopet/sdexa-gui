"""Based on a script of Burak Aybar (burak.aybar@tum.de) who also provided the pretrained model"""

import pytorch_lightning
import segmentation_models_pytorch


class BaseModel(pytorch_lightning.LightningModule):
    """Class for loading and executing the pytorch model."""
    def __init__(self):
        super(BaseModel, self).__init__()
        self.seed = 42
        self.model = segmentation_models_pytorch.Unet(
            in_channels=1,
            classes=1,
        )

    def forward(self, image):
        """Apply the model to the image."""
        return self.model(image.float())
