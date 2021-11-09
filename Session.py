class Session:
    def __init__(self, user_id, start_date):
        self.user_id = user_id
        self.start_date = start_date
        self.surview = None
        self.projection = None
        self.show_surview_segmentation = False

    def get_start_date(self):
        return self.start_date

    def set_surview(self, surview):
        self.surview = surview

    def has_surview(self):
        return self.surview is not None

    def get_surview_image(self):
        if not self.has_surview():
            return None
        return self.surview.get_image()

    def get_full_surview_image(self):
        if not self.has_surview():
            return None
        return self.surview.get_full_image()

    def show_surview_segmentation(self):
        self.show_surview_segmentation = True

    def hide_surview_segmentation(self):
        self.show_surview_segmentation = False

    def switch_surview_segmentation(self):
        self.show_surview_segmentation = not self.show_surview_segmentation

    def set_surview_image_position(self, position_x, position_y):
        self.surview.set_image_position((position_x, position_y))

    def get_surview_segmentation_overlay_image(self):
        if not self.has_surview():
            return None
        return self.surview.get_segmentation_overlay_image()

    def get_surview_image_csv(self):
        if not self.has_surview():
            return None
        return self.surview.get_image_csv()

    def get_surview_segmentation_csv(self):
        if not self.has_surview():
            return None
        return self.surview.get_segmentation_csv()

    def set_projection(self, ct_projection):
        self.projection = ct_projection

    def has_projection(self):
        return self.projection is not None

    def get_projection_image(self):
        if self.projection is None:
            return None
        return self.projection.get_image()

    def get_full_projection_image(self):
        if self.projection is None:
            return None
        return self.projection.get_full_image()

    def set_projection_image_position(self, position_x, position_y):
        self.projection.set_image_position((position_x, position_y))
