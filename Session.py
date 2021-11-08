import os
from datetime import datetime
from PIL import Image


# TODO
class Session:
    def __init__(self, user_id, directory):
        self.user_id = user_id
        self.directory = directory
        self.surview = None
        self.ct_projection = None
        self.filename_surview = None
        self.filename_ct_projection = None

    def set_surview(self, surview):
        self.cleanup_surview_file()
        self.surview = surview

    def get_surview_image(self):
        if self.surview is None:
            return None
        if self.filename_surview is not None:
            return self.filename_surview
        self.generate_new_surview_file(self.surview.get_image())
        return self.filename_surview

    def get_full_surview_image(self):
        if self.surview is None:
            return None
        return self.surview.get_full_image()

    def overlay_surview_image_with_segmentation(self):
        if self.surview is None:
            return None
        self.generate_new_surview_file(self.surview.get_segmentation_overlay_image())

    def get_surview_image_csv(self):
        if self.surview is None:
            return None
        return self.surview.get_image_csv()

    def get_surview_segmentation_csv(self):
        if self.surview is None:
            return None
        return self.surview.get_segmentation_csv()

    def generate_new_surview_file(self, image):
        filename = self.get_timestamped_image_file(image)
        self.filename_surview = filename

    def cleanup_surview_file(self):
        if self.filename_surview is None:
            return
        os.remove(self.directory + self.filename_surview)
        self.filename_surview = None

    def set_ct_projection(self, ct_projection):
        self.cleanup_ct_projection_file()
        self.ct_projection = ct_projection

    def get_ct_projection_image(self):
        if self.ct_projection is None:
            return None
        if self.filename_ct_projection is not None:
            return self.filename_ct_projection
        return self.generate_ct_projection_file()

    def generate_ct_projection_file(self):
        filename = self.get_timestamped_image_file(self.ct_projection.get_image())
        self.filename_ct_projection = filename
        return filename

    def cleanup_ct_projection_file(self):
        if self.filename_ct_projection is None:
            return
        os.remove(self.directory + self.filename_ct_projection)
        self.filename_ct_projection = None

    def get_timestamped_image_file(self, image):
        filename = datetime.now().strftime("%y%m%d%H%M%S")
        path = os.path.join(self.directory, filename + '.jpeg')
        Image.fromarray(image).save(path)
        return filename + '.jpeg'
