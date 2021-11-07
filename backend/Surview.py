from io import StringIO, BytesIO
import numpy as np
from backend.helpers import to_uint8, to_normalized_rgb, to_normalized_uint8_rgb
from backend.segmentation.Segmentation import perform_segmentation


class Surview:
    def __init__(self, file, cropping=(0, 0), window=None):
        x, y = cropping
        self.surview = np.loadtxt(file, delimiter=",")[x:x + 512, y:y + 512]
        self.window = window
        self.segmentation = None

    def get_image(self):
        return to_normalized_uint8_rgb(self.surview, self.window)

    def get_segmentation_overlay_image(self):
        return self.overlay_images()

    def get_segmentation_csv(self):
        segmentation = self.get_segmentation()
        stream = StringIO()
        np.savetxt(stream, to_uint8(segmentation), fmt="%i", delimiter=",")
        csv_string = stream.getvalue()
        return BytesIO(csv_string.encode())

    def get_segmentation(self):
        if self.segmentation is None:
            self.segmentation = perform_segmentation(self.surview)
        return self.segmentation

    def overlay_images(self, mask_intensity=50):
        image = to_normalized_rgb(self.surview, self.window)
        image[:, :, 0] += self.get_segmentation() * mask_intensity
        return to_uint8(image)
