from flask import request, session
from backend.Projection import Projection
from server import *


class ProjectionService(WebService):
    """Handles REST routes for the projection image."""
    def __init__(self, user_service):
        super().__init__(user_service)
        self.routes = [
            Route('/projection', self.get_projection, ["GET"]),
            Route('/projection', self.upload_projection, ["POST"]),
            Route('/projection', self.delete_projection, ["DELETE"]),
            Route('/projection/full', self.get_full_projection, ["GET"]),
            Route('/projection/position', self.set_projection_position, ["PUT"]),
            Route('/projection/window', self.set_projection_window, ["PUT"]),
            Route('/projection/download', self.download_projection_image, ["GET"]),
            Route('/projection/registration', self.switch_projection_registration_view, ["PUT"]),
            Route('/projection/registration/download', self.download_projection_registration, ["GET"]),
        ]

    def get_projection(self):
        user_session = self.user_service.get_user_session(session)
        if not user_session.has_projection():
            return NOT_FOUND
        if user_session.show_projection_registration:
            if not user_session.has_surview():
                return ERROR
            image = user_session.get_projection_registration_overlay_image()
        else:
            image = user_session.get_projection_image()
        return self.send_jpeg(image)

    def delete_projection(self):
        user_session = self.user_service.get_user_session(session)
        user_session.delete_projection()
        return SUCCESS

    def get_full_projection(self):
        user_session = self.user_service.get_user_session(session)
        if not user_session.has_projection():
            return NOT_FOUND
        return self.send_jpeg(user_session.get_full_projection_image())

    def upload_projection(self):
        user_session = self.user_service.get_user_session(session)
        if not request.files.get('file'):
            return 'File is missing!', 400
        file = request.files['file']
        try:
            projection = Projection(file)
        except Exception as exception:
            return str(exception), 400
        user_session.set_projection(projection)
        user_session.hide_projection_registration()
        return SUCCESS

    def set_projection_position(self):
        user_session = self.user_service.get_user_session(session)
        if not user_session.has_projection():
            return ERROR
        user_session.set_projection_image_position(request.json['posX'], request.json['posY'])
        return SUCCESS

    def set_projection_window(self):
        user_session = self.user_service.get_user_session(session)
        if not user_session.has_projection():
            return ERROR
        minimum = self.string_to_float(request.json['min'])
        maximum = self.string_to_float(request.json['max'])
        user_session.set_projection_window((minimum, maximum))
        return SUCCESS

    def download_projection_image(self):
        user_session = self.user_service.get_user_session(session)
        if not user_session.has_projection():
            return NOT_FOUND
        csv = user_session.get_projection_image_csv()
        return self.send_csv(csv)

    def switch_projection_registration_view(self):
        user_session = self.user_service.get_user_session(session)
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        user_session.switch_projection_registration()
        return SUCCESS

    def download_projection_registration(self):
        user_session = self.user_service.get_user_session(session)
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        csv = user_session.get_projection_registration_csv()
        return self.send_csv(csv)
