import uuid
from datetime import datetime, timedelta
from flask import session
from server.UserSession import UserSession


class UserService:
    """Manage UserSessions using flask sessions.
    """
    def __init__(self):
        self.sessions = {}

    def get_session(self) -> UserSession:
        """Gets the UserSession belonging to the request.
        If no UserSession exists creates a new one and set the user_id of the flask session.
        :returns the UserSession.
        """
        if 'user_id' not in session or self.sessions.get(session['user_id']) is None:
            session['user_id'] = self.generate_new_session().user_id
        return self.sessions[session['user_id']]

    def generate_new_session(self) -> UserSession:
        """Generates a new UserSession with unique user_id.
        Important: Cleans up all sessions older than one day in order to avoid running out of memory.
        :returns the created UserSession
        """
        self.cleanup_old_sessions()
        user_id = uuid.uuid4().hex
        new_session = UserSession(user_id, datetime.now())
        self.sessions[user_id] = new_session
        return new_session

    def cleanup_old_sessions(self):
        """Cleans up all sessions older than one day.
        """
        for key, user_session in self.sessions.items():
            if user_session.get_start_date() < (datetime.now() - timedelta(days=1)):
                self.sessions.pop(key)
