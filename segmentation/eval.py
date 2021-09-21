import pytorch_lightning as pl

from argparse import ArgumentParser
from omegaconf import OmegaConf

from model.base import BaseModel
from pytorch_lightning import Trainer

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--config_path", default='./configs/base_config.yaml', help="Path to the config file", type=str)
    parser.add_argument("--ckpt_path", default='./checkpoints/0912_194939.ckpt', help="Model checkpoint path", type=str)
    hparams = parser.parse_args()

    config_path = hparams.config_path
    ckpt_path = hparams.ckpt_path

    hparams = OmegaConf.load(config_path)

    trainer = Trainer(
        gpus=0,
        callbacks=None,
        logger=False
    )

    model = BaseModel.load_from_checkpoint(ckpt_path, hparams=hparams)

    trainer.test(model)