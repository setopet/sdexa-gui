"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from server.Server import Server
from flask import Flask
from config import load_dev_config


def register_routes(server):
    for route in server.routes:
        app.add_url_rule(route.path, view_func=route.handle, methods=route.methods)


app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/static',
            template_folder='frontend/templates')

load_dev_config(app)
register_routes(Server())

if __name__ == "__main__":
    app.run()
