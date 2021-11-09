import uuid
from datetime import datetime, timedelta
from flask import session
from Session import Session


class UserService:
    def __init__(self):
        self.sessions = {}

    def get_session(self) -> Session:
        if 'user_id' not in session or self.sessions.get(session['user_id']) is None:
            session['user_id'] = self.generate_new_session().user_id
        return self.sessions[session['user_id']]

    def generate_new_session(self) -> Session:
        user_id = uuid.uuid4().hex
        new_session = Session(user_id, datetime.now())
        self.sessions[user_id] = new_session
        return new_session

    def cleanup_old_sessions(self):
        for key, user_session in self.sessions.items():
            if user_session.get_start_date() < (datetime.now() - timedelta(days=1)):
                self.sessions.pop(key)