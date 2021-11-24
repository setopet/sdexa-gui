"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from io import BytesIO
from PIL import Image
from flask import send_file


class WebService:
    """Super class for WebServices. Provides methods for request handling."""
    def __init__(self, request_context, user_service):
        self.request_context = request_context
        self.user_service = user_service

    def get_json_values(self, *args):
        json_values = []
        json = self.request_context.get().json
        for arg in args:
            json_values.append(json[arg])
        return json_values

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
    def get_file(request):
        if not request.files.get('file'):
            return 'File is missing!', 400
        return request.files['file']

    @staticmethod
    def string_to_float(string):
        try:
            return float(string)
        except:
            return None

    @staticmethod
    def string_to_int(string):
        try:
            return int(string)
        except:
            return None

