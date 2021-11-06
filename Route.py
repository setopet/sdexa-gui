class Route:
    def __init__(self, path, handle, methods=None):
        if methods is None:
            methods = ["GET"]
        self.path = path
        self.handle = handle
        self.methods = methods