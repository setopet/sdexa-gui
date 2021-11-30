"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import unittest
from unittest.mock import Mock, PropertyMock
from server import SUCCESS, ProjectionService
from tests.server.app import get_app
from tests.helpers import *


class ImageServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = get_app()

    def setUp(self):
        self.user_session = Mock(name="user_session_mock")
        self.user_service = Mock(name="user_service_mock")
        self.user_service.get_user_session.return_value = self.user_session
        self.request_context = Mock(name="request_context_mock")
        self.projection_service = ProjectionService(self.request_context, self.user_service)

    def test_gets_image(self):
        with self.app.test_request_context():
            image_mock = Mock()
            image_mock.get_image.return_value=np.ones((512, 512, 3)).astype('uint8')
            property_mock = PropertyMock(return_value=image_mock)
            type(self.user_session).projection = property_mock
            result = self.projection_service.get_projection_image()
            self.assertEqual(result.content_type, 'image/jpeg')
            self.assertEqual(result.status_code, SUCCESS[1])

    def test_uploads_image(self):
        self.request_context.get.return_value.files = {'file': 'this is a file'}
        self.projection_service.upload_projection_image()
        self.user_session.set_projection.assert_called_with('this is a file')

    def test_downloads_image(self):
        with self.app.test_request_context():
            image_mock = Mock()
            image_mock.get_image_csv.return_value = get_txt_from_array(ones.astype('uint8')).getvalue()
            property_mock = PropertyMock(return_value=image_mock)
            type(self.user_session).projection = property_mock
            result = self.projection_service.download_projection_image()
            self.assertTrue("text/csv" in result.content_type)
            self.assertEqual(result.status_code, SUCCESS[1])

