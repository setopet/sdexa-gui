"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from flask import session


class SessionContext:
    def get(self):
        return session
