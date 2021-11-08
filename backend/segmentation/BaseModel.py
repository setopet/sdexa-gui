import pytorch_lightning as pl
import segmentation_models_pytorch as smp


# Credits to Burak Aybar (TUM) for providing the pretrained model
class BaseModel(pl.LightningModule):
    def __init__(self):
        super(BaseModel, self).__init__()
        self.seed = 42
        self.model = smp.Unet(
            in_channels=1,  # model input channels (1 for gray-scale images, 3 for RGB, etc.)
            classes=1,  # model output channels (number of classes in your dataset)
        )

    def forward(self, x):
        return self.model(x.float())  # .float() is necessary, because pytorch expects type 'double' otherwise
