import os

import numpy as np
from datetime import datetime
from PIL import Image


# normalize array, set minimum to 0 and maximum to 255
def normalize_array(image: np.array) -> np.array:
    result = image - image.min()
    return result * (255 / result.max())


# save image in upload directory with timestamped filename
def save_image(path, image) -> str:
    filename = datetime.now().strftime("%y%m%d%H%M%S")
    path = os.path.join(path, filename + '.jpeg')
    Image.fromarray(image).save(path)
    return filename + '.jpeg'
