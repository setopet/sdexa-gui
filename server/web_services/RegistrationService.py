"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from server import *


class RegistrationService(WebService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/projection/registration', self.switch_projection_registration_view, ["PUT"]),
            Route('/projection/registration/download', self.download_projection_registration, ["GET"])
        ]

    def switch_projection_registration_view(self):
        user_session = self.user_service.get_user_session()
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        user_session.switch_projection_registration()
        return SUCCESS

    def download_projection_registration(self):
        user_session = self.user_service.get_user_session()
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        csv = user_session.get_projection_registration_csv()
        return self.send_csv(csv)