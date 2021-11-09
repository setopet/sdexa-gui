from backend.processing import get_array_from_file, insert_padding, crop_image, to_normalized_uint8_rgb, image_to_csv


class Image:
    def __init__(self, file, window=None):
        self.full_image = get_array_from_file(file).squeeze()
        self.image = self.set_image_position((0, 0))
        self.window = window

    def set_image_position(self, position):
        image = insert_padding(self.full_image)
        self.image = crop_image(position, image)
        return self.image

    def get_image(self):
        return to_normalized_uint8_rgb(self.image, self.window)

    def get_full_image(self):
        return to_normalized_uint8_rgb(self.full_image, self.window)

    def get_image_csv(self):
        return image_to_csv(self.image)
