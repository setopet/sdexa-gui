from server.Server import Server
from flask import Flask
from Config import config

app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/static',
            template_folder='frontend/templates'
            )


def init_routes(server):
    """Registers all routes of the server.
    """
    for route in server.routes:
        app.add_url_rule(route.path, view_func=route.handle, methods=route.methods)


def init():
    config(app)
    init_routes(Server())


init()

if __name__ == "__main__":
    app.run()
