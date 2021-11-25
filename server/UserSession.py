"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import Projection


# TODO: Teilweise überflüsstig, sollte nur noch surview, projection setzen und einfache Checks zur Verfügung stellen
#  keine None-Checks und reines Durchreichen von "set image position" etc.. Das können die Services direkt machen
class UserSession:
    """Saves and modifies the state of the application for an user."""
    def __init__(self, user_id, start_date):
        self.user_id = user_id
        self._start_date = start_date
        self._surview = None
        self.projection = None  # TODO: Property draus machen
        self.show_projection_registration = False

    @property
    def surview(self):
        return self._surview

    @surview.setter
    def surview(self, surview):
        self._surview = surview

    @surview.deleter
    def surview(self):
        self._surview = None

    @property
    def start_date(self):
        return self._start_date

    def has_surview(self):
        return self._surview is not None

    def has_scatter(self):
        return self.has_surview() and self._surview.scatter is not None

    def set_projection(self, file):
        self.projection = Projection(file)

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
        self.projection.set_image_region((position_x, position_y))

    def set_projection_window(self, window):
        self.projection.set_window(window)

    def get_projection_image_csv(self):
        if self.projection is None:
            return None
        return self.projection.get_image_csv()

    def get_projection_registration_overlay_image(self):
        if self.projection is None or self._surview is None:
            return None
        return self.projection.get_registration_overlay_image(self._surview.get_surview_array())

    def get_projection_registration_csv(self):
        if self.projection is None or self._surview is None:
            return None
        return self.projection.get_registration_result_csv(self._surview.get_surview_array())
