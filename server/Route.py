"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""


class Route:
    """Represents a REST route.
    :param path: path of the route.
    :param handle: the handler function of the route
    :param methods: HTTP methods associated with the route.
    """
    def __init__(self, path, handle, methods):
        self.path = path
        self.handle = handle
        self.methods = methods
