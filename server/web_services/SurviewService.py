"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from backend import Surview
from server import *


# TODO: Verallgemeinern zu 'ImageService'
class SurviewService(WebService):
    """Handles REST routes for the surview image."""
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview', self.get_surview, ["GET"]),
            Route('/surview', self.upload_surview, ["POST"]),
            Route('/surview', self.delete_surview, ["DELETE"]),
            Route('/surview/full', self.get_full_surview, ["GET"]),
            Route('/surview/position', self.set_surview_position, ["PUT"]),
            Route('/surview/window', self.set_surview_window, ["PUT"]),
            Route('/surview/download', self.download_surview_image, ["GET"])
        ]

    def get_surview(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return NOT_FOUND
        return self.send_jpeg(surview.get_image())

    def delete_surview(self):
        user_session = self.user_service.get_user_session()
        del user_session.surview
        return SUCCESS

    def get_full_surview(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return NOT_FOUND
        return self.send_jpeg(surview.get_full_image())

    def upload_surview(self):
        user_session = self.user_service.get_user_session()
        request = self.request_context.get()
        file = self.get_file(request)
        try:
            surview = Surview(file)
            user_session.surview = surview
        except Exception as exception:
            return str(exception), 400
        return SUCCESS

    def set_surview_position(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return ERROR
        request = self.request_context.get()
        surview.set_image_position((request.json['posX'], request.json['posY']))
        return SUCCESS

    def set_surview_window(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return ERROR
        request = self.request_context.get()
        minimum = self.string_to_float(request.json['min'])
        maximum = self.string_to_float(request.json['max'])
        surview.set_window((minimum, maximum))
        return SUCCESS

    def download_surview_image(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return NOT_FOUND
        csv = surview.get_image_csv()
        return self.send_csv(csv)
