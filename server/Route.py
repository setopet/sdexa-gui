class Route:
    """Represents a REST route.
    :param path: path of the route.
    :param handle: the handler function of the route
    :param methods: HTTP methods associated with the route. Takes "GET" as default if not specified.
    """
    def __init__(self, path, handle, methods=None):
        if methods is None:
            methods = ["GET"]
        self.path = path
        self.handle = handle
        self.methods = methods
