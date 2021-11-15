from backend import *


class Projection(Image):
    """Loads and manages the projection image.
    """
    def __init__(self, file, window=None):
        super().__init__(file, window)
        self.registration_result = None
        return

    def get_registration_overlay_image(self, surview):
        return overlay_with_mask(surview, self.get_registration_mask(surview), 50, self.window)

    def get_registration_result_csv(self, surview):
        return image_to_csv(self.get_registration_mask(surview), format_string="%i")

    def get_registration_mask(self, surview):
        return create_mask(perform_registration(surview, self.image), 15)
