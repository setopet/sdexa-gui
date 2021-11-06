import os

from flask import Flask, render_template, request, send_file

from backend.CtProjection import CtProjection
from backend.Surview import Surview

app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/static',
            template_folder='frontend/templates'
            )
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['FILENAME_SURVIEW'] = None
app.config['FILENAME_CT'] = None


@app.route('/', methods=['GET'])
def root():
    return get_root_page()


@app.route('/uploads/<image>', methods=['GET'])
def get_image(image=None):
    return send_file('uploads/' + image, mimetype='image/jpeg')


@app.route('/surview', methods=['POST'])
def upload_surview():
    if not request.files.get('file'):
        return
    file = request.files['file']
    surview = Surview(file, (0, 800))
    app.config['FILENAME_SURVIEW'] = surview.get_segmentation_overlay_image(UPLOAD_DIR)
    return upload_successful()


@app.route('/ct-projection', methods=['POST'])
def upload_ct_projection():
    if not request.files.get('file'):
        return
    file = request.files['file']
    ct_projection = CtProjection(file)
    app.config['FILENAME_CT'] = ct_projection.get_registration_result(UPLOAD_DIR)
    return upload_successful()


def get_root_page():
    filename_surview = app.config['FILENAME_SURVIEW']
    filename_ct = app.config['FILENAME_CT']
    return render_template('index.html',
                           filename_surview=filename_surview,
                           filename_ct= filename_ct)


def upload_successful():
    return '', 200


if __name__ == '__main__':
    app.run()
