import logging
import numpy as np
import torch
import cv2

from os import listdir
from glob import glob
from torch.utils.data import Dataset
from PIL import Image
from torchvision.transforms import transforms


class BasicDataset(Dataset):
    def __init__(self, data, transform=None, eval=False):
        self.imgs_dir = data.dataset.image_path
        self.masks_dir = data.dataset.image_path if eval else data.dataset.mask_path
        self.transform = transform

        self.ids = [file.split('.')[0] for file in listdir(self.imgs_dir)
                    if not file.startswith('.')]
        logging.info(f'Creating dataset with {len(self.ids)} examples')

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        idx = self.ids[i]
        img_file = glob(self.imgs_dir + idx + '*')
        mask_file = glob(self.masks_dir + idx + '*')

        img = cv2.imread(img_file[0], 0)
        mask = cv2.imread(mask_file[0], 0)

        if self.transform:
            img = self.transform(img)
            mask = self.transform(mask)

        assert len(mask_file) == 1, \
            f'Either no mask or multiple masks found for the ID {idx}: {mask_file}'
        assert len(img_file) == 1, \
            f'Either no image or multiple images found for the ID {idx}: {img_file}'

        return img, mask, idx
