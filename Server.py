from io import BytesIO

from PIL import Image
from flask import render_template, request, send_file

from Session import Session
from api import SUCCESS, NOT_FOUND
from Route import Route
from backend.CtProjection import CtProjection
from backend.Surview import Surview
from Config import CONFIG

DEFAULT_USER_ID = 1


class Server:
    def __init__(self):
        self.routes = [
            Route('/', self.get_root_page, ["GET"]),
            Route('/surview', self.upload_surview, ["POST"]),
            Route('/ct-projection', self.upload_ct_projection, ["POST"]),
            Route('/uploads/<image>', self.get_image, ["GET"]),
            Route('/surview/full', self.get_full_surview, ["GET"]),
            Route('/surview/segmentation', self.perform_surview_segmention, ["PUT"]),
            Route('/surview/download', self.download_surview_image, ["GET"]),
            Route('/surview/segmentation/download', self.download_surview_segmentation, ["GET"])
        ]
        self.session = None
        self.directory = CONFIG['UPLOAD_DIR']

    def get_root_page(self):
        filename_surview = None
        filename_ct = None
        if self.session is not None:
            filename_surview = self.session.get_surview_image()
            filename_ct = self.session.get_ct_projection_image()
        return render_template('index.html',
                               filename_surview=filename_surview,
                               filename_ct=filename_ct)

    # TODO: Das hier auch nicht mehr über Files machen sondern In-Memory-Streams
    def get_image(self, image=None):
        return send_file(self.directory + "/" + image, mimetype='image/jpeg')

    def get_full_surview(self):
        full_surview = self.session.get_full_surview_image()
        return send_jpeg(full_surview)

    def upload_surview(self):
        if not request.files.get('file'):
            return
        file = request.files['file']
        surview = Surview(file, cropping=(0, 0), window=(0, 2000))
        session = self.session
        if session is None:
            session = self.generate_new_session()
        session.set_surview(surview)
        return SUCCESS

    def perform_surview_segmention(self):
        if self.session is None or self.session.get_surview_image() is None:
            return NOT_FOUND
        self.session.overlay_surview_image_with_segmentation()
        return SUCCESS

    def download_surview_image(self):
        csv = self.session.get_surview_image_csv()
        if csv is None:
            return NOT_FOUND
        return send_csv(csv)

    def download_surview_segmentation(self):
        csv = self.session.get_surview_segmentation_csv()
        if csv is None:
            return NOT_FOUND
        return send_csv(csv)

    def upload_ct_projection(self):
        if not request.files.get('file'):
            return
        file = request.files['file']
        ct_projection = CtProjection(file)
        session = self.session
        if self.session is None:
            session = self.generate_new_session()
        session.set_ct_projection(ct_projection)
        return SUCCESS

    def generate_new_session(self):
        self.session = Session(DEFAULT_USER_ID, self.directory)
        return self.session


# Flask accepts only byte encoded File-like objects for "send_file"
def send_csv(csv):
    return send_file(BytesIO(csv.encode()), mimetype="text/csv")


def send_jpeg(image):
    stream = BytesIO()
    Image.fromarray(image).save(stream, format='JPEG')
    stream.seek(0)
    return send_file(stream, mimetype='image/jpeg')