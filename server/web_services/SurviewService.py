"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import Image, Surview
from server import *


class SurviewService(ImageService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview', self.get_surview_image, ["GET"]),
            Route('/surview', self.upload_surview_image, ["POST"]),
            Route('/surview', self.delete_surview_image, ["DELETE"]),
            Route('/surview/full', self.get_full_surview_image, ["GET"]),
            Route('/surview/position', self.set_surview_image_position, ["PUT"]),
            Route('/surview/window', self.set_surview_image_window, ["PUT"]),
            Route('/surview/download', self.download_surview_image, ["GET"])
        ]

    def get_image_from_session(self) -> Image:
        user_session = self.user_service.get_user_session()
        return user_session.surview

    def set_image_on_session(self, file):
        user_session = self.user_service.get_user_session()
        user_session.set_surview(file)

    def delete_image_from_session(self):
        user_session = self.user_service.get_user_session()
        if user_session.projection is not None:
            user_session.projection.delete_registration()
        del user_session.surview

    def get_surview_image(self):
        return self.get_image()

    def upload_surview_image(self):
        return self.upload_image()

    def delete_surview_image(self):
        return self.delete_image()

    def get_full_surview_image(self):
        return self.get_full_image()

    def set_surview_image_position(self):
        return self.set_image_position()

    def set_surview_image_window(self):
        return self.set_image_window()

    def download_surview_image(self):
        return self.download_image()
