"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import Projection, Surview


class UserSession:
    """Saves the state of the application for an user."""
    def __init__(self, user_id, start_date):
        self.user_id = user_id
        self._start_date = start_date
        self.__surview = None
        self.__projection = None
        self.show_projection_registration = False

    @property
    def surview(self):
        return self.__surview

    @surview.deleter
    def surview(self):
        self.__surview = None

    @property
    def projection(self):
        return self.__projection

    @projection.deleter
    def projection(self):
        self.__projection = None

    @property
    def start_date(self):
        return self._start_date#

    def set_projection(self, file):
        self.__projection = Projection(file)

    def set_surview(self, file):
        self.__surview = Surview(file)

    def has_surview(self):
        return self.__surview is not None

    def has_scatter(self):
        return self.has_surview() and self.__surview.scatter is not None

    def has_projection(self):
        return self.projection is not None

    def has_registration(self):
        return self.projection is not None and self.projection.registration is not None
