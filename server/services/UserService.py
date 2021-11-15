import uuid
from datetime import datetime, timedelta
from flask import session
from server.UserSession import UserSession


class UserService:
    """Manages UserSessions.
    """
    def __init__(self):
        self.sessions = {}

    def get_session(self) -> UserSession:
        """Gets the UserSession belonging to the request.
        Creates a new one if the UserSession does not exist.
        :returns the UserSession.
        """
        if 'user_id' not in session or self.sessions.get(session['user_id']) is None:
            session['user_id'] = self.generate_new_session().user_id
        return self.sessions[session['user_id']]

    def generate_new_session(self) -> UserSession:
        """Generates a new UserSession.
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
