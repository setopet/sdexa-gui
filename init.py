import os
from Server import Server
from flask import Flask
from Config import load_config, CONFIG


app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/static',
            template_folder='frontend/templates'
            )


def init_routes(server):
    for route in server.routes:
        app.add_url_rule(route.path, view_func=route.handle, methods=route.methods)


def init_file_system():
    os.makedirs(CONFIG['UPLOAD_DIR'], exist_ok=True)


def init():
    load_config()
    init_file_system()
    init_routes(Server())


init()

if __name__ == "__main__":
    app.run()
