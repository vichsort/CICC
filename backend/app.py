from flask import Flask
from backend.routes.api import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
