"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import Projection


class UserSession:
    """Saves and modifies the state of the application for an user."""
    def __init__(self, user_id, start_date):
        self.user_id = user_id
        self._start_date = start_date
        self.__surview = None
        self.__projection = None
        self.show_projection_registration = False

    @property
    def surview(self):
        return self.__surview

    @surview.setter
    def surview(self, surview):
        self.__surview = surview

    @surview.deleter
    def surview(self):
        self.__surview = None

    @property
    def projection(self):
        return self.__projection

    @projection.setter
    def projection(self, projection):
        self.__projection = projection

    @projection.deleter
    def projection(self):
        self.__projection = None

    @property
    def start_date(self):
        return self._start_date

    def has_surview(self):
        return self.__surview is not None

    def has_scatter(self):
        return self.has_surview() and self.__surview.scatter is not None

    def set_projection(self, file):
        self.projection = Projection(file)

    def has_projection(self):
        return self.projection is not None

    def has_registration(self):
        return self.projection is not None and self.projection.registration is not None

    def get_projection_image(self):
        if self.projection is None:
            return None
        return self.projection.get_image()

    def delete_projection(self):
        self.projection = None

