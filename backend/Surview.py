from backend.processing import to_uint8, to_normalized_uint8_rgb, image_to_csv, get_array_from_file, \
    insert_padding, crop_image, overlay_with_mask
from backend.segmentation.Segmentation import perform_segmentation


class Surview:
    def __init__(self, file, window=None):
        self.full_image = get_array_from_file(file).squeeze()
        self.image = self.set_image_position((0, 0))
        self.window = window
        self.segmentation = None

    def set_image_position(self, positions):
        image = insert_padding(self.full_image)
        self.image = crop_image(positions, image)
        return image

    def get_image(self):
        return to_normalized_uint8_rgb(self.image, self.window)

    def get_full_image(self):
        return to_normalized_uint8_rgb(self.full_image, self.window)

    def get_segmentation_overlay_image(self):
        return overlay_with_mask(self.image, self.get_segmentation(), 50, self.window)

    def get_segmentation_csv(self):
        return image_to_csv(to_uint8(self.get_segmentation()), format_string="%i")

    def get_image_csv(self):
        return image_to_csv(self.image)

    def get_segmentation(self):
        if self.segmentation is None:
            self.segmentation = perform_segmentation(self.image)
        return self.segmentation
