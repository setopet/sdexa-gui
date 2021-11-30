"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from flask import Flask
from config import load_dev_config


def get_app():
    root_path = "../../"
    app = Flask(__name__,
                static_url_path='',
                template_folder=root_path + 'frontend/templates',
                static_folder=root_path + 'frontend/static')
    load_dev_config(app)
    return app
