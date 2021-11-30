"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import Image, Projection
from server import *


class ProjectionService(ImageService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/projection', self.get_projection_image, ["GET"]),
            Route('/projection', self.upload_projection_image, ["POST"]),
            Route('/projection', self.delete_projection_image, ["DELETE"]),
            Route('/projection/full', self.get_full_projection_image, ["GET"]),
            Route('/projection/position', self.set_projection_image_position, ["PUT"]),
            Route('/projection/window', self.set_projection_image_window, ["PUT"]),
            Route('/projection/download', self.download_projection_image, ["GET"])
        ]

    def get_image_from_session(self) -> Image:
        user_session = self.user_service.get_user_session()
        return user_session.projection

    def set_image_on_session(self, file):
        user_session = self.user_service.get_user_session()
        user_session.set_projection(file)

    def delete_image_from_session(self):
        user_session = self.user_service.get_user_session()
        del user_session.projection

    def get_projection_image(self):
        return self.get_image()

    def upload_projection_image(self):
        return self.upload_image()

    def delete_projection_image(self):
        return self.delete_image()

    def get_full_projection_image(self):
        return self.get_full_image()

    def set_projection_image_position(self):
        return self.set_image_position()

    def set_projection_image_window(self):
        return self.set_image_window()

    def download_projection_image(self):
        return self.download_image()
