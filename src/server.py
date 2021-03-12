"""Main application bootstrap"""

import pathlib

from flask import Flask

import src.routes as routes
import src.libs.session as session
from src.swagger import swagger_router

PATH = pathlib.Path(__file__).parent.absolute()

app = Flask(__name__, static_folder=f"{PATH}/static")
session.setup_session(app)

app.register_blueprint(swagger_router)
app.register_blueprint(routes.ping_router)
