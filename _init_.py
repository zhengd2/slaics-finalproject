import pathlib

from flask import Flask
from crud import create


def init_db():
    create.callback("data_for_final", "data_for_final.csv")


def create_app():
    app = Flask(__name__)
    if not pathlib.Path("data_for_final.sqlite3").exists():
        init_db()
    from logic import main

    app.register_blueprint(main)

    return app