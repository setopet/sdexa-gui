import cv2
import torch
import torchvision
import yaml
import pandas as pd
import pydicom
import glob
import numpy as np

from pathlib import Path
from itertools import repeat
from PIL import Image

from segmentation.model.metric import dice_score


def transform_to_hu(medical_image, image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    hu_image = image * slope + intercept

    return hu_image


def load_images(folder_name):
    files = glob.glob(folder_name + '/**/S1**/I10', recursive=True)


def read_dicom(fname):
    return pydicom.read_file(fname)


def read_yaml(fname):
    fname = Path(fname)
    with fname.open('rt') as handle:
        return yaml.load(handle, yaml.FullLoader)


def write_yaml(content, fname):
    fname = Path(fname)
    with fname.open('wt') as handle:
        yaml.dump(content, handle, default_flow_style=False)


def inf_loop(data_loader):
    """ wrapper function for endless data loader. """
    for loader in repeat(data_loader):
        yield from loader


def save_image(output, idx, save_path):
    for i in range(output.shape[0]):
        torchvision.utils.save_image(output[i], '{}/{}.png'.format(save_path, idx[i]))


def save_image_with_score(x, y, y_hat, file_path):
    for i in range(x.shape[0]):
        score = dice_score(y_hat[i], y[i])

        input = x[i, :, :, :]
        label = y[i, :, :, :]
        pred = y_hat[i, :, :, :]
        out = torch.cat((input, label, pred), 1)
        out = out.mul(255).add_(0.5).clamp_(0, 255).flip(2).permute(2, 1, 0).to('cpu', torch.uint8).numpy()
        img = out.copy()
        cv2.putText(img, str(round(score.item(), 2)), (1220,50), 2, 2, 255)

        cv2.imwrite('./results/with_scores/{}.png'.format(file_path[i]), img)
        # torchv,ision.utils.save_image(out, './results/{}.png'.format(file_path[i]))
        # image = Image.fromarray(np_array.astype(np.uint8))
        # image.save(file_path)


class MetricTracker:
    def __init__(self, *keys, writer=None):
        self.writer = writer
        self._data = pd.DataFrame(index=keys, columns=['total', 'counts', 'average'])
        self.reset()

    def reset(self):
        for col in self._data.columns:
            self._data[col].values[:] = 0

    def update(self, key, value, n=1):
        if self.writer is not None:
            self.writer.add_scalar(key, value)
        self._data.total[key] += value * n
        self._data.counts[key] += n
        self._data.average[key] = self._data.total[key] / self._data.counts[key]

    def avg(self, key):
        return self._data.average[key]

    def result(self):
        return dict(self._data.average)