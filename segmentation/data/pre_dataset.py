import logging
import numpy as np
import pandas as pd
import re
import os

from os import listdir
from glob import glob
from torch.utils.data import Dataset
from preprocessing import read_image, preprocess_image
from PIL import Image
from tqdm import tqdm


class PreDataset(Dataset):
    def __init__(self, imgs_dir: str, masks_dir: str, masks):
        self.imgs_dir = imgs_dir
        self.masks_dir = masks_dir
        self.masks = masks

        self._clean_data()

        self.ids = [file.split('.')[0] for file in listdir(imgs_dir)
                    if not file.startswith('.')]
        logging.info(f'Creating dataset with {len(self.ids)} examples')

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        idx = self.ids[i]
        mask_file = glob(self.masks_dir + idx + '*')
        img_file = glob(self.imgs_dir + idx + '*')

        img, img_header = read_image(img_file[0])
        mask, mask_header = read_image(mask_file[0], mask=True)

        assert len(mask_file) == 1, \
            f'Either no mask or multiple masks found for the ID {idx}: {mask_file}'
        assert len(img_file) == 1, \
            f'Either no image or multiple images found for the ID {idx}: {img_file}'

        img = preprocess_image(img, img_header)
        mask = preprocess_image(mask, mask_header, mask=True, masks=self.masks)

        assert img.size == mask.size, \
            f'Image and mask {idx} should be the same size, but are {img.size} and {mask.size}'

        return {'image': img, 'mask': mask, 'filename': idx + '.png'}

    def _clean_data(self):
        filenames = glob('data/verse*.json')
        for file in filenames:
            data = pd.read_json(file)

            if not data.label.isin(self.masks).any():
                file = re.split('/|_', file)[1]
                for filename in glob(self.dir_img + file + '*'):
                    os.remove(filename)
                for filename in glob(self.dir_mask + file + '*'):
                    os.remove(filename)

    def save(cls, output_dir: str):
        with tqdm(total=len(cls)) as pbar:
            for i in range(len(cls)):
                data = cls[i]

                image = data['image']
                im = Image.fromarray(image.astype(np.uint8))
                im.save(output_dir + 'imgs/' + data['filename'])

                mask = data['mask']
                im = Image.fromarray(mask.astype(np.uint8))
                im.save(output_dir + 'masks/' + data['filename'])

                pbar.update()
