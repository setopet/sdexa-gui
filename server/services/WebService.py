from io import BytesIO
from PIL import Image
from flask import send_file


class WebService:
    def __init__(self, user_service):
        self.user_service = user_service

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
