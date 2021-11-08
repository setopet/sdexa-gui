from backend.Image import Image
from backend.processing import create_mask, overlay_with_mask, image_to_csv
from backend.registration.registration import perform_registration


class CtProjection(Image):
    def __init__(self, file, window=None):
        super().__init__(file, window)
        self.registration_result = None
        return

    def get_registration_overlay_image(self, surview):
        return overlay_with_mask(surview, self.get_registration_mask(surview), 50, self.window)

    def get_registration_result(self, surview):
        return perform_registration(surview, self.image)

    def get_registration_result_csv(self, surview):
        return image_to_csv(self.get_registration_mask(surview), format_string="%i")

    def get_registration_mask(self, surview):
        return create_mask(self.get_registration_result(surview), 15)
