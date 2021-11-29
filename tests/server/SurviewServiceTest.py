"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import unittest
import numpy as np
from unittest.mock import Mock
from server import SUCCESS, ImageService
from tests.server.test_app import get_test_app


class SurviewServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = get_test_app()

    def setUp(self):
        self.user_session = Mock(name="user_session_mock")
        self.user_service = Mock(name="user_service_mock")
        self.user_service.get_user_session.return_value = self.user_session
        self.request_context = Mock(name="request_context_mock")
        self.surview_service = ImageService(self.request_context, self.user_service)

    # TODO: Nach Refactoring hat sich die Aufrufstruktur geändert
    def test_gets_surview(self):
        self.user_session.has_surview.return_value = True
        self.user_session.show_surview_segmentation = False
        self.user_session.get_surview_image.return_value = np.ones((512, 512, 3)).astype('uint8')
        with self.app.test_request_context():
            result = self.surview_service.get_image()
            self.assertEqual(result.content_type, 'image/jpeg')
            self.assertEqual(result.status_code, SUCCESS[1])

    # TODO: Nach Refactoring hat sich die Aufrufstruktur geändert
    def test_uploads_surview(self):
        self.request_context.get.return_value.files = {'file': 'this is a file'}
        self.surview_service.upload_image()
        self.user_session.set_surview.assert_called_with('this is a file')
