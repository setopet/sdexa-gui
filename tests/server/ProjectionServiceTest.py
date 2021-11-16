import unittest
import numpy as np
from unittest.mock import Mock
from server import SUCCESS, ProjectionService
from tests.server.test_app import get_test_app


class ProjectionServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = get_test_app()

    def setUp(self):
        self.user_session = Mock(name="user_session_mock")
        self.user_service = Mock(name="user_service_mock")
        self.user_service.get_user_session.return_value = self.user_session
        self.request_context = Mock(name="request_context_mock")
        self.projection_service = ProjectionService(self.request_context, self.user_service)

    def test_gets_projection(self):
        self.user_session.has_projection.return_value = True
        self.user_session.show_projection_registration = False
        self.user_session.get_projection_image.return_value = np.ones((512, 512, 3)).astype('uint8')
        with self.app.test_request_context():
            result = self.projection_service.get_projection()
            self.assertEqual(result.content_type, 'image/jpeg')
            self.assertEqual(result.status_code, SUCCESS[1])

    def test_uploads_projection(self):
        self.request_context.get.return_value.files = {'file': 'this is a file'}
        self.projection_service.upload_projection()
        self.user_session.set_projection.assert_called_with('this is a file')
