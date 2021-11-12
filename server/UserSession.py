class UserSession:
    def __init__(self, user_id, start_date):
        self.user_id = user_id
        self.start_date = start_date
        self.surview = None
        self.projection = None
        self.show_surview_segmentation = False
        self.show_projection_registration = False

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

    def delete_surview(self):
        self.surview = None

    def get_full_surview_image(self):
        if not self.has_surview():
            return None
        return self.surview.get_full_image()

    def hide_surview_segmentation(self):
        self.show_surview_segmentation = False

    def switch_surview_segmentation(self):
        self.show_surview_segmentation = not self.show_surview_segmentation

    def set_surview_image_position(self, position_x, position_y):
        self.surview.set_image_position((position_x, position_y))

    def set_surview_window(self, window):
        self.surview.set_window(window)

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

    def delete_projection(self):
        self.projection = None

    def get_full_projection_image(self):
        if self.projection is None:
            return None
        return self.projection.get_full_image()

    def hide_projection_registration(self):
        self.show_projection_registration = False

    def switch_projection_registration(self):
        self.show_projection_registration = not self.show_projection_registration

    def set_projection_image_position(self, position_x, position_y):
        self.projection.set_image_position((position_x, position_y))

    def set_projection_window(self, window):
        self.projection.set_window(window)

    def get_projection_image_csv(self):
        if self.projection is None:
            return None
        return self.projection.get_image_csv()

    def get_projection_registration_overlay_image(self):
        if self.projection is None or self.surview is None:
            return None
        return self.projection.get_registration_overlay_image(self.surview.get_surview_array())

    def get_projection_registration_csv(self):
        if self.projection is None or self.surview is None:
            return None
        return self.projection.get_registration_result_csv(self.surview.get_surview_array())
