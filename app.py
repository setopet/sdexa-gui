import os
from datetime import datetime

import numpy
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config['UPLOAD_DIR'] = 'uploads'


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', image_filename=None)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['upload']
    image = normalize_array(np.load(file))
    mask = get_segmentation(image)
    filename = save_image(overlay_images(image, mask))
    return render_template('index.html', image_filename=filename + '.jpeg')


# save image in upload directory with timestamped filename
def save_image(image):
    filename = datetime.now().strftime("%y%m%d%H%M%S")
    path = os.path.join(app.config['UPLOAD_DIR'], filename + '.jpeg')
    Image.fromarray(image).save(path)
    return filename


# overlay image with mask
def overlay_images(image, mask):
    result = np.stack([image, image, image]).transpose(2, 3, 0, 1).squeeze()
    result[:, :, 0] += mask.squeeze() * 100  # multiplying mask with value between 1 and 255 for better displaying
    return result.astype('uint8')


# normalize array, set minimum to 0 and maximum to 255
def normalize_array(image: numpy.array):
    result = image - image.min()
    return result * (255 / result.max())


# will be removed for real segmentation (Burak's code)
# mask contains only ones and zeros.
def get_segmentation(array: numpy.array):
    mask_path = 'C:\\Users\\Sebastian\\LRZ Sync+Share\\Informatik\\Bachelorarbeit\\Daten\\Surview_data\\' \
                'S002768_S1000_output-photo_r1_mask.npy'
    return np.load(mask_path)


@app.route('/uploads/<image>', methods=['GET'])
def get_image(image=None):
    return send_file('uploads/' + image, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run()
