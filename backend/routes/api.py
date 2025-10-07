from flask import Blueprint
from backend.routes.emission_record import emission_record

api = Blueprint('api', __name__)

api.register_blueprint(emission_record, url_prefix='/emission')
