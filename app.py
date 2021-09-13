from flask import Flask, render_template, request, send_file
from CtDataHandler import CtDataHandler
from SurviewDataHandler import SurviewDataHandler

app = Flask(__name__)
app.config['UPLOAD_DIR'] = 'uploads'
sv_handler = SurviewDataHandler(app.config['UPLOAD_DIR'])
ct_handler = CtDataHandler(app.config['UPLOAD_DIR'])


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', surview_filename=None)


@app.route('/uploads/<image>', methods=['GET'])
def get_image(image=None):
    return send_file('uploads/' + image, mimetype='image/jpeg')


@app.route('/upload', methods=['POST'])
def upload_surview():
    filename_surview = None
    filename_ct = None

    if request.files.get('surview'):
        file = request.files['surview']
        filename_surview = sv_handler.process_and_save_image(file)

    if request.files.get('ct'):
        file = request.files['ct']
        filename_ct = ct_handler.process_and_save_image(file)
    return render_template('index.html', filename_surview=filename_surview, filename_ct=filename_ct)


if __name__ == '__main__':
    app.run()
