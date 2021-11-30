"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from flask import session


class SessionContext:
    """Gets the session context."""
    def get(self):
        return session
