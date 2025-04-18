"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import unittest
from server.Server import Server
from tests.server.app import get_app


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = get_app()

    def test_returns_home_page(self):
        server = Server()
        with self.app.test_request_context():
            self.assertRegex(server.get_root_page(), "<!doctype html>")
