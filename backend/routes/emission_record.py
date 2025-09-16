from flask import Blueprint, request
from ..database.database import db

emission_record = Blueprint('emission', __name__)

@emission_record.route('/', methods=['POST'])
def create_emission_record():
    data = request.json

    