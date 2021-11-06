from flask import render_template, request, send_file
from api import SUCCESS_RESPONSE
from Route import Route
from backend.CtProjection import CtProjection
from backend.Surview import Surview


class Server:
    def __init__(self, app):
        self.app = app
        self.routes = [
            Route('/', self.get_root_page, ["GET"]),
            Route('/surview', self.upload_surview, ["POST"]),
            Route('/ct-projection', self.upload_ct_projection, ["POST"]),
            Route('/uploads/<image>', self.get_image, ["GET"])
        ]

    def get_root_page(self):
        filename_surview = self.app.config['FILENAME_SURVIEW']
        filename_ct = self.app.config['FILENAME_CT']
        return render_template('index.html',
                               filename_surview=filename_surview,
                               filename_ct= filename_ct)

    def get_image(self, image=None):
        return send_file(self.app.config['UPLOAD_DIR'] + "/" + image, mimetype='image/jpeg')

    def upload_surview(self):
        if not request.files.get('file'):
            return
        file = request.files['file']
        surview = Surview(file, (0, 800))
        self.app.config['FILENAME_SURVIEW'] = surview.get_segmentation_overlay_image(self.app.config['UPLOAD_DIR'])
        return SUCCESS_RESPONSE

    def upload_ct_projection(self):
        if not request.files.get('file'):
            return
        file = request.files['file']
        ct_projection = CtProjection(file)
        self.app.config['FILENAME_CT'] = ct_projection.get_registration_result(self.app.config['UPLOAD_DIR'])
        return SUCCESS_RESPONSE

