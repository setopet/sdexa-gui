"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from server import *


class RegistrationService(WebService):
    """Handles REST routes for the registration of the projection"""
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/projection/registration', self.get_projection_registration, ["GET"]),
            Route('/projection/registration/download', self.download_projection_registration, ["GET"])
        ]

    def get_projection_registration(self):
        user_session = self.user_service.get_user_session()
        projection = user_session.projection
        if not (projection is not None and user_session.has_surview()):
            return NOT_FOUND
        return self.send_jpeg(projection.get_registration_overlay_image(user_session.surview.get_surview_array()))

    def download_projection_registration(self):
        user_session = self.user_service.get_user_session()
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        csv = user_session.get_projection_registration_csv()
        return self.send_csv(csv)