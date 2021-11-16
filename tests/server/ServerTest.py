import unittest

from flask import Flask

from Config import CONFIG
from server.Server import Server


class ServerTest(unittest.TestCase):
    # TODO: Set up von mock flask app auslagern
    # TODO: Außerdem wohl doch lieber die Testmodule in eigenen Ordner außerhalb des Source-Codes haben
    def setUp(self):
        root_path = "../../"
        self.flask_app = Flask(__name__, template_folder=root_path + 'frontend/templates')
        CONFIG['BASE_URL'] = "42"
        self.flask_app.secret_key = "42"

    def test_returns_home_page(self):
        server = Server()
        with self.flask_app.test_request_context():
            self.assertRegex(server.get_root_page(), "<!doctype html>")
