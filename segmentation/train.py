from omegaconf import OmegaConf
import pytorch_lightning as pl

from argparse import ArgumentParser
from datetime import datetime

from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

from model.base import BaseModel


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--config_path", default='./configs/base_config.yaml', help="Path to the config file", type=str)
    hparams = parser.parse_args()

    config_path = hparams.config_path

    hparams = OmegaConf.load(config_path)

    checkpoint_file_name = datetime.now().strftime(r'%m%d_%H%M%S')
    print(checkpoint_file_name)

    model = BaseModel(hparams)

    early_stop_callback = EarlyStopping(monitor='val/score', patience=50, mode='max')
    checkpoint_callback = ModelCheckpoint(
        monitor='val/score',
        dirpath='checkpoints/',
        filename=checkpoint_file_name,
        mode='max',
    )

    trainer = Trainer(
        gpus=hparams.trainer.gpus,
        max_epochs=hparams.trainer.max_epochs,
        callbacks=[early_stop_callback, checkpoint_callback]
    )

    trainer.fit(model)

    trainer = Trainer(
        gpus=1
    )

    model = BaseModel.load_from_checkpoint(checkpoint_path='./checkpoints/' + checkpoint_file_name + '.ckpt',
                                               hparams=hparams)

    trainer.test(model)