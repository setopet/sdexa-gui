import os
import torch
import pytorch_lightning as pl
import segmentation_models_pytorch as smp

from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Subset
from torchvision.transforms import transforms
from torchvision.utils import make_grid
from utils.util import save_image
from data.dataset import BasicDataset
from model.metric import dice_score
from model.losses import DiceLoss

class BaseModel(pl.LightningModule):
    def __init__(self, hparams):
        super(BaseModel, self).__init__()
        self.seed = hparams.seed
        self.data = hparams.data
        self.loader = hparams.data.loader
        self.optimizer = hparams.optimizer
        self.val = hparams.eval
        self.save_path = hparams.save_path
        self.n_channels = 1
        self.use_batch_norm = True
        self.phase = ''

        self.image_path = self.data.dataset.image_path
        self.mask_path = self.data.dataset.mask_path

        os.makedirs(self.save_path, exist_ok=True)

        self.model = smp.Unet(
            in_channels=1,  # model input channels (1 for gray-scale images, 3 for RGB, etc.)
            classes=1,  # model output channels (number of classes in your dataset)
        )

        trans = transforms.Compose([
            transforms.ToTensor(),
        ])

        dataset = BasicDataset(self.data, transform=trans, eval=self.val)

        if self.val:
            self.test_dataset = dataset
        else:
            train_dataset, self.test_dataset = self.__train_val_dataset(dataset)
            self.train_dataset, self.val_dataset = self.__train_val_dataset(train_dataset, val_split=0.25)

    # Split the given dataset with given percentage
    def __train_val_dataset(self, dataset, val_split=0.2):
        train_idx, val_idx = train_test_split(list(range(len(dataset))), test_size=val_split, random_state=self.seed)
        return Subset(dataset, train_idx), Subset(dataset, val_idx)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        return self.run_step(batch, 'train')

    def validation_step(self, batch, batch_idx):
        return self.run_step(batch, 'val')

    def test_step(self, batch, batch_idx):
        return self.run_step(batch, 'test')

    def run_step(self, batch, tag):
        input, label, idx = batch

        output = self.forward(input)
        output = torch.sigmoid(output)

        criterion = DiceLoss()
        loss = criterion(output, label)

        score = dice_score(output, label)

        self.log(f'{tag}/loss', loss)
        self.log(f'{tag}/score', score)

        if self.logger:
            self.logger.experiment.add_image(f'{tag}/input', make_grid(input))
            self.logger.experiment.add_image(f'{tag}/mask_org', make_grid(label))
            self.logger.experiment.add_image(f'{tag}/mask_pred', make_grid(output))

        if self.val:
            save_image(output, idx, self.save_path)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.optimizer.lr)
        return [optimizer]

    # DataLoader with training samples.
    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.loader.batch_size,
                          shuffle=True, num_workers=self.loader.num_workers, pin_memory=True)

    # DataLoader with validation samples.
    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.loader.batch_size, shuffle=False,
                          num_workers=self.loader.num_workers)

    # DataLoader with test samples.
    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.loader.batch_size, shuffle=False,
                          num_workers=self.loader.num_workers)

    def get_progress_bar_dict(self):
        # don't show the version number
        items = super().get_progress_bar_dict()
        items.pop("v_num", None)
        return items