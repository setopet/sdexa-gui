from backend.Image import Image
from backend.processing import create_mask, overlay_with_mask


class CtProjection(Image):
    def __init__(self, file, window=None):
        super().__init__(file, window)
        return

    def get_registration_overlay_image(self, surview):
        mask = create_mask(self.get_registration_result(), 15)
        return overlay_with_mask(surview, mask, 50, self.window)

    def get_registration_result(self):
        pass
