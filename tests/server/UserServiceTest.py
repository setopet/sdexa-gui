import unittest
import server
from datetime import datetime, timedelta
from unittest.mock import Mock


class UserServiceTest(unittest.TestCase):
    def setUp(self):
        self.session_context = Mock()
        self.user_service = server.UserService(self.session_context)

    def test_creates_new_session(self):
        self.session_context.get.return_value = {}
        user_session = self.user_service.get_user_session()
        self.assertIsInstance(user_session, server.UserSession)

    def test_returns_known_session(self):
        self.session_context.get.return_value = {}
        user_session = self.user_service.get_user_session()
        self.session_context.get.return_value = {'user_id': user_session.user_id}
        returned_session = self.user_service.get_user_session()
        self.assertEqual(user_session, returned_session)

    def test_removes_old_sessions(self):
        self.session_context.get.return_value = {}
        user_session = self.user_service.get_user_session()
        user_session.start_date = datetime.now() - timedelta(days=2)
        self.session_context.get.return_value = {}
        self.user_service.get_user_session()  # first session should be cleaned up when creating a second one
        self.session_context.get.return_value = {'user_id': user_session.user_id}
        self.assertNotEqual(self.user_service.get_user_session(), user_session)
