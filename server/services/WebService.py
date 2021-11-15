from io import BytesIO
from PIL import Image
from flask import send_file


class WebService:
    """Super class for WebServices.
    """
    def __init__(self, user_service):
        self.user_service = user_service

    @staticmethod
    def send_csv(csv):
        # Flask accepts only byte-encoded File-like objects for "send_file"
        return send_file(BytesIO(csv.encode()), mimetype="text/csv")

    @staticmethod
    def send_jpeg(image):
        stream = BytesIO()
        Image.fromarray(image).save(stream, format='JPEG')
        stream.seek(0)
        return send_file(stream, mimetype='image/jpeg')

    @staticmethod
    def string_to_float(string):
        try:
            return float(string)
        except:
            return None

