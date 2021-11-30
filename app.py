"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from server.Server import Server
from flask import Flask
from config import CONFIG


app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/static',
            template_folder='frontend/templates')

for route in Server().routes:
    app.add_url_rule(route.path, view_func=route.handle, methods=route.methods)

app.secret_key = CONFIG['SECRET_KEY']

if __name__ == "__main__":
    app.run()
