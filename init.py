import os
from Server import Server
from flask import Flask

from config import config


# TODO: Das hier nicht mehr global sichtbar machen und insbesondere die Zustandsverwaltung
#  nicht mehr über app.config
app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/static',
            template_folder='frontend/templates'
            )


def init_routes(server):
    for route in server.routes:
        app.add_url_rule(route.path, view_func=route.handle, methods=route.methods)


def init_file_system():
    os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)


def init():
    config(app)
    init_file_system()
    server = Server(app)
    init_routes(server)


init()

if __name__ == "__main__":
    app.run()
