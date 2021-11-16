from flask import request


class RequestContext:
    def get(self):
        return request
