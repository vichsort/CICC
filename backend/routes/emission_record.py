from flask import Blueprint, request, jsonify
from backend.database.database import db
from backend.utils.emission_calculator import calculate_emission

emission_record = Blueprint('emission', __name__)

@emission_record.route('/', methods=['POST'])
def create_emission_record():
    data = request.json

    person_name = data.get('person_name')
    distance = data.get('distance')
    people_amount = data.get('people_amount', None)
    vehicle = data.get('vehicle')
    fuel = data.get('fuel')

    if 'vehicle_type' in data:
        vehicle += f'-{data.get('vehicle_type')}'

    emission = calculate_emission(vehicle, fuel, int(people_amount), float(distance))

    db.query(
        'INSERT INTO public.emission_records ' \
        '(person_name, emission_amount, distance, people_amount, vehicle, fuel) ' \
        'VALUES (%s, %s, %s, %s, %s, %s);',
        (
            person_name,
            emission,
            distance,
            people_amount,
            vehicle,
            fuel
        )
    )

    return jsonify(
        {
            'ok': True,
            'message': f'Emission record created for {person_name}. Calculated emission: {emission} kg CO₂.'
        }
    ), 201
