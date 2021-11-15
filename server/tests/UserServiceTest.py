import unittest
import server
from datetime import datetime, timedelta


class UserServiceTest(unittest.TestCase):
    def test_creates_new_session(self):
        user_service = server.UserService()
        session = user_service.get_user_session({})
        self.assertIsNotNone(session)
        self.assertIsInstance(session, server.UserSession)

    def test_returns_known_session(self):
        user_service = server.UserService()
        session = user_service.get_user_session({})
        returned_session = user_service.get_user_session({'user_id': session.user_id})
        self.assertEqual(session, returned_session)

    def test_removes_old_sessions(self):
        user_service = server.UserService()
        session = user_service.get_user_session({})
        session.start_date = datetime.now() - timedelta(days=2)
        user_service.get_user_session({})
        self.assertNotEqual(user_service.get_user_session({'user_id': session.user_id}), session)

