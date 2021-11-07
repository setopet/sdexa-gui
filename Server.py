from flask import render_template, request, send_file

from Session import Session
from api import SUCCESS_RESPONSE
from Route import Route
from backend.CtProjection import CtProjection
from backend.Surview import Surview
from Config import Config

DEFAULT_USER_ID = 1


class Server:
    def __init__(self):
        self.routes = [
            Route('/', self.get_root_page, ["GET"]),
            Route('/surview', self.upload_surview, ["POST"]),
            Route('/ct-projection', self.upload_ct_projection, ["POST"]),
            Route('/uploads/<image>', self.get_image, ["GET"])
        ]
        self.session = None
        self.directory = Config['UPLOAD_DIR']

    def get_root_page(self):
        filename_surview = None
        filename_ct = None
        if self.session is not None:
            filename_surview = self.session.get_surview_file()
            filename_ct = self.session.get_ct_projection_file()
        return render_template('index.html',
                               filename_surview=filename_surview,
                               filename_ct=filename_ct)

    # TODO: Get Request zu Bildern mit UserId als Parameter anstatt filenames
    def get_image(self, image=None):
        return send_file(self.directory + "/" + image, mimetype='image/jpeg')

    def upload_surview(self):
        if not request.files.get('file'):
            return
        file = request.files['file']
        surview = Surview(file, (0, 800))
        session = self.session
        if session is None:
            session = self.generate_new_session()
        session.set_surview(surview)
        return SUCCESS_RESPONSE

    def upload_ct_projection(self):
        if not request.files.get('file'):
            return
        file = request.files['file']
        ct_projection = CtProjection(file)
        session = self.session
        if self.session is None:
            session = self.generate_new_session()
        session.set_ct_projection(ct_projection)
        return SUCCESS_RESPONSE

    def generate_new_session(self):
        self.session = Session(DEFAULT_USER_ID, self.directory)
        return self.session
