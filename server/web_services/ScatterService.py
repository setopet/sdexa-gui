"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from server import *


class ScatterService(WebService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview/scatter', self.upload_scatter, ["POST"]),
            Route('/surview/scatter', self.delete_scatter, ["DELETE"])
        ]

    def upload_scatter(self):
        user_session = self.user_service.get_user_session()
        request = self.request_context.get()
        surview = user_session.surview
        if surview is None:
            return ERROR
        file = self.get_file(request)
        try:
            surview.set_scatter(file)
        except Exception as exception:
            return str(exception), 400
        return SUCCESS

    def delete_scatter(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return SUCCESS
        surview.delete_scatter()
        return SUCCESS

