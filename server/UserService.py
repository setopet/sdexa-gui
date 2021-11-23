import uuid
from datetime import datetime, timedelta
from server import *


class UserService:
    """Manages the sessions of all users for the server."""
    def __init__(self, session_context):
        self.user_sessions = {}
        self.session_context = session_context

    def get_user_session(self):
        """Gets the UserSession belonging to the request.
        Creates a new one if the UserSession does not exist.
        :returns the UserSession.
        """
        session = self.session_context.get()
        if 'user_id' not in session or self.user_sessions.get(session['user_id']) is None:
            session['user_id'] = self.generate_new_session().user_id
        return self.user_sessions[session['user_id']]

    def generate_new_session(self):
        """Generates a new UserSession.
        Important: Cleans up all sessions older than one day in order to avoid running out of memory.
        :returns the created UserSession
        """
        self.cleanup_old_sessions()
        user_id = uuid.uuid4().hex
        new_session = UserSession(user_id, datetime.now())
        self.user_sessions[user_id] = new_session
        return new_session

    def cleanup_old_sessions(self):
        """Cleans up all sessions older than one day."""
        sessions = list(self.user_sessions.items())
        for key, user_session in sessions:
            if user_session.get_start_date() < (datetime.now() - timedelta(days=1)):
                self.user_sessions.pop(key)
