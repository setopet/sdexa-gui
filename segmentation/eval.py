import numpy as np
import pytorch_lightning as pl
import cv2
from argparse import ArgumentParser
import pytorch_lightning as pl

import torchvision
from torchvision.transforms import transforms

import torch
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

    model = BaseModel.load_from_checkpoint(ckpt_path, hparams=hparams)
    test = cv2.imread('G:\\Code\\ba\\thesis-gui\\segmentation\\inputs\\S002768_S1000_output-photo.png', 0)
    res = model(transforms.ToTensor()(test)[None, ...])
    torchvision.utils.save_image(res, '{}\\{}.png'.format('G:\\Code\\ba\\thesis-gui\\segmentation\\outputs\\', 'out'))
