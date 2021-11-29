"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from abc import abstractmethod

from backend import Surview, Image
from server import *


class ImageService(WebService):
    """Handles REST routes for the surview image."""
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)

    @abstractmethod
    def get_image_from_session(self) -> Image:
        ...

    @abstractmethod
    def set_image_on_session(self, image):
        ...

    @abstractmethod
    def delete_image_from_session(self):
        ...

    def get_image(self):
        image = self.get_image_from_session()
        if image is None:
            return NOT_FOUND
        return self.send_jpeg(image.get_image())

    def delete_image(self):
        self.delete_image_from_session()
        return SUCCESS

    def get_full_image(self):
        image = self.get_image_from_session()
        if image is None:
            return NOT_FOUND
        return self.send_jpeg(image.get_full_image())

    def upload_image(self):
        request = self.request_context.get()
        file = self.get_file(request)
        try:
            self.set_image_on_session(file)
        except Exception as exception:
            return str(exception), 400
        return SUCCESS

    def set_image_position(self):
        image = self.get_image_from_session()
        if image is None:
            return ERROR
        region = tuple(map(self.string_to_int, self.get_json_values("posX", "posY", "dx", "dy")))
        image.set_image_region(region)
        return SUCCESS

    def set_image_window(self):
        image = self.get_image_from_session()
        if image is None:
            return ERROR
        request = self.request_context.get()
        minimum = self.string_to_float(request.json['min'])
        maximum = self.string_to_float(request.json['max'])
        image.set_window((minimum, maximum))
        return SUCCESS

    def download_image(self):
        image = self.get_image_from_session()
        if image is None:
            return NOT_FOUND
        csv = image.get_image_csv()
        return self.send_csv(csv)
