from server import *


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
            Route('/surview/download', self.download_surview_image, ["GET"]),
            Route('/surview/segmentation', self.switch_surview_segmention_view, ["PUT"]),
            Route('/surview/segmentation/download', self.download_surview_segmentation, ["GET"])
        ]

    def get_surview(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return NOT_FOUND
        if user_session.show_surview_segmentation:
            image = user_session.get_surview_segmentation_overlay_image()
        else:
            image = user_session.get_surview_image()
        return self.send_jpeg(image)

    def delete_surview(self):
        user_session = self.user_service.get_user_session()
        user_session.delete_surview()
        user_session.hide_projection_registration()
        return SUCCESS

    def get_full_surview(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return NOT_FOUND
        return self.send_jpeg(user_session.get_full_surview_image())

    def upload_surview(self):
        user_session = self.user_service.get_user_session()
        request = self.request_context.get()
        if not request.files.get('file'):
            return 'File is missing!', 400
        file = request.files['file']
        try:
            user_session.set_surview(file)
        except Exception as exception:
            return str(exception), 400
        user_session.hide_surview_segmentation()
        return SUCCESS

    def set_surview_position(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return ERROR
        request = self.request_context.get()
        user_session.set_surview_image_position(request.json['posX'], request.json['posY'])
        return SUCCESS

    def set_surview_window(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return ERROR
        request = self.request_context.get()
        minimum = self.string_to_float(request.json['min'])
        maximum = self.string_to_float(request.json['max'])
        user_session.set_surview_window((minimum, maximum))
        return SUCCESS

    def switch_surview_segmention_view(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return ERROR
        user_session.switch_surview_segmentation()
        return SUCCESS

    def download_surview_image(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return NOT_FOUND
        csv = user_session.get_surview_image_csv()
        return self.send_csv(csv)

    def download_surview_segmentation(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return NOT_FOUND
        csv = user_session.get_surview_segmentation_csv()
        return self.send_csv(csv)
