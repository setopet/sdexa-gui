from io import BytesIO
from PIL import Image
from flask import render_template, request, send_file, Response
from Config import CONFIG
from api import SUCCESS, NOT_FOUND, ERROR
from Route import Route
from backend.Projection import Projection
from backend.Surview import Surview


class Server:
    def __init__(self, user_service):
        self.user_service = user_service
        self.routes = [
            Route('/', self.get_root_page, ["GET"]),
            Route('/surview', self.get_surview, ["GET"]),
            Route('/surview', self.upload_surview, ["POST"]),
            Route('/surview/full', self.get_full_surview, ["GET"]),
            Route('/surview/position', self.set_surview_position, ["PUT"]),
            Route('/surview/download', self.download_surview_image, ["GET"]),
            Route('/surview/segmentation', self.switch_surview_segmention_view, ["PUT"]),
            Route('/surview/segmentation/download', self.download_surview_segmentation, ["GET"]),
            Route('/projection', self.get_projection, ["GET"]),
            Route('/projection', self.upload_projection, ["POST"]),
            Route('/projection/full', self.get_full_projection, ["GET"]),
            Route('/projection/position', self.set_projection_position, ["PUT"]),
            Route('/projection/download', self.download_projection_image, ["GET"]),
            Route('/projection/registration', self.switch_projection_registration_view, ["PUT"]),
            Route('/projection/registration/download', self.download_projection_registration, ["GET"]),
        ]

    def get_root_page(self):
        user_session = self.user_service.get_session()
        return render_template('index.html',
                               base_url=CONFIG['BASE_URL'],
                               surview_present=user_session.has_surview(),
                               projection_present=user_session.has_projection())

    def get_surview(self):
        user_session = self.user_service.get_session()
        if not user_session.has_surview():
            return NOT_FOUND
        if user_session.show_surview_segmentation:
            image = user_session.get_surview_segmentation_overlay_image()
        else:
            image = user_session.get_surview_image()
        return self.send_jpeg(image)

    def get_full_surview(self):
        user_session = self.user_service.get_session()
        if not user_session.has_surview():
            return NOT_FOUND
        return self.send_jpeg(user_session.get_full_surview_image())

    def upload_surview(self):
        user_session = self.user_service.get_session()
        if not request.files.get('file'):
            return 'File is missing!', 400
        file = request.files['file']
        try:
            surview = Surview(file, window=(0, 2000))
        except Exception as exception:
            return str(exception), 400
        user_session.set_surview(surview)
        user_session.hide_surview_segmentation()
        return SUCCESS

    def set_surview_position(self):
        user_session = self.user_service.get_session()
        if not user_session.has_surview():
            return ERROR
        user_session.set_surview_image_position(request.json['posX'], request.json['posY'])
        return SUCCESS

    def switch_surview_segmention_view(self):
        user_session = self.user_service.get_session()
        if not user_session.has_surview():
            return ERROR
        user_session.switch_surview_segmentation()
        return SUCCESS

    def download_surview_image(self):
        user_session = self.user_service.get_session()
        if not user_session.has_surview():
            return NOT_FOUND
        csv = user_session.get_surview_image_csv()
        return self.send_csv(csv)

    def download_surview_segmentation(self):
        user_session = self.user_service.get_session()
        if not user_session.has_surview():
            return NOT_FOUND
        csv = user_session.get_surview_segmentation_csv()
        return self.send_csv(csv)

    def get_projection(self):
        user_session = self.user_service.get_session()
        if not user_session.has_projection():
            return NOT_FOUND
        if user_session.show_projection_registration:
            if not user_session.has_surview():
                return ERROR
            image = user_session.get_projection_registration_overlay_image()
        else:
            image = user_session.get_projection_image()
        return self.send_jpeg(image)

    def get_full_projection(self):
        user_session = self.user_service.get_session()
        if not user_session.has_projection():
            return NOT_FOUND
        return self.send_jpeg(user_session.get_full_projection_image())

    def upload_projection(self):
        user_session = self.user_service.get_session()
        if not request.files.get('file'):
            return 'File is missing!', 400
        file = request.files['file']
        try:
            projection = Projection(file)
        except Exception as exception:
            return str(exception), 400
        user_session.set_projection(projection)
        return SUCCESS

    def set_projection_position(self):
        user_session = self.user_service.get_session()
        if not user_session.has_projection():
            return ERROR
        user_session.set_projection_image_position(request.json['posX'], request.json['posY'])
        return SUCCESS

    def download_projection_image(self):
        user_session = self.user_service.get_session()
        if not user_session.has_projection():
            return NOT_FOUND
        csv = user_session.get_projection_image_csv()
        return self.send_csv(csv)

    def switch_projection_registration_view(self):
        user_session = self.user_service.get_session()
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        user_session.switch_projection_registration()
        return SUCCESS

    def download_projection_registration(self):
        user_session = self.user_service.get_session()
        if not (user_session.has_projection() and user_session.has_surview()):
            return ERROR
        csv = user_session.get_projection_registration_csv()
        return self.send_csv(csv)

    # Flask accepts only byte-encoded File-like objects for "send_file"
    @staticmethod
    def send_csv(csv):
        return send_file(BytesIO(csv.encode()), mimetype="text/csv")

    @staticmethod
    def send_jpeg(image):
        stream = BytesIO()
        Image.fromarray(image).save(stream, format='JPEG')
        stream.seek(0)
        return send_file(stream, mimetype='image/jpeg')
