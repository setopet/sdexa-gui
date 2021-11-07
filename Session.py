import os
from datetime import datetime
from PIL import Image


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

    def get_surview(self):
        return self.surview

    def get_surview_file(self):
        if self.surview is None:
            return None
        if self.filename_surview is not None:
            return self.filename_surview
        return self.generate_surview_file()

    # TODO: Methoden die z.B. die Segmentierung auslösen ändern das filename_surview zu overlay
    def generate_surview_file(self):
        surview = self.surview.get_segmentation_overlay_image()
        filename = self.get_timestamped_image_file(surview)
        self.filename_surview = filename
        return filename

    def cleanup_surview_file(self):
        if self.filename_surview is None:
            return
        os.remove(self.directory + self.filename_surview)
        self.filename_surview = None

    def set_ct_projection(self, ct_projection):
        self.cleanup_ct_projection_file()
        self.ct_projection = ct_projection

    def get_ct_projection(self):
        return self.ct_projection

    def get_ct_projection_file(self):
        if self.ct_projection is None:
            return None
        if self.filename_ct_projection is not None:
            return self.filename_ct_projection
        return self.generate_ct_projection_file()

    def generate_ct_projection_file(self):
        projection = self.ct_projection.get_ct_projection()
        filename = self.get_timestamped_image_file(projection)
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
