"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from flask import request


class RequestContext:
    def get(self):
        return request
