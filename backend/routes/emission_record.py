from flask import Blueprint

emission_record = Blueprint('emission', __name__)

@emission_record.route('/', methods=['POST'])
def create_emission_record():
    pass