from server import *


class ScatterService(WebService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview/scatter', self.upload_scatter, ["POST"])
        ]

    def upload_scatter(self):
        user_session = self.user_service.get_user_session()
        request = self.request_context.get()
        if not user_session.has_surview:
            return ERROR
        file = self.get_file(request)
        try:
            user_session.set_surview_scatter_image(file)
        except Exception as exception:
            return str(exception), 400
        return SUCCESS
