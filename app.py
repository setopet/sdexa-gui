import os

from flask import Flask, render_template, request, send_file
from CtDataHandler import CtDataHandler
from Surview import Surview

app = Flask(__name__)
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['FILENAME_SURVIEW'] = None
app.config['FILENAME_CT'] = None
ct_handler = CtDataHandler(UPLOAD_DIR)


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', filename_surview=None, filename_ct=None)


@app.route('/uploads/<image>', methods=['GET'])
def get_image(image=None):
    return send_file('uploads/' + image, mimetype='image/jpeg')


@app.route('/uploads', methods=['POST'])
def upload_surview():
    if request.files.get('surview'):
        file = request.files['surview']
        surview = Surview(file, (0, 800))
        app.config['FILENAME_SURVIEW'] = surview.get_segmentation_overlay_image(UPLOAD_DIR)
    if request.files.get('ct'):
        file = request.files['ct']
        app.config['FILENAME_CT'] = ct_handler.process_and_save_image(file)
    return render_template('index.html', filename_surview=app.config['FILENAME_SURVIEW'], filename_ct=app.config['FILENAME_CT'])


if __name__ == '__main__':
    app.run()
