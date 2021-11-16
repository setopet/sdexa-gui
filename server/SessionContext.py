from flask import session


class SessionContext:
    def get(self):
        return session
