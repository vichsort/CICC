"""
Módulo para o registro de emissões de carbono.

Este módulo define rotas da API Flask delegando toda a lógica de persistência
e cálculos para a camada de serviço (emission_service).
"""

from flask import Blueprint, request, jsonify
from backend.services.emission_service import emission_service
from backend.utils.emission_calculator import calculate_emission

# Cria um Blueprint do Flask para organizar as rotas de emissão.
emission_record = Blueprint('emission', __name__)


@emission_record.route('/', methods=['POST'])
def create_emission_record():
    """
    Cria e armazena um novo registro de emissão de CO₂.
    """
    data = request.json or {}

    distance = data.get('distance')
    people_amount = data.get('people_amount', None)
    vehicle = data.get('vehicle')
    fuel = data.get('fuel')
    vehicle_type = data.get('vehicle_type')

    if not distance or not vehicle or not fuel:
        return jsonify({'ok': False, 'message': 'Campos obrigatórios ausentes.'}), 400

    # Concatena o tipo do veículo ao veículo principal, se existir.
    if vehicle_type:
        vehicle += "-" + str(vehicle_type)

    # Para o cálculo, se não for um ônibus, considera pelo menos 1 pessoa.
    calculation_people_amount = None
    if 'bus' not in vehicle:
        calculation_people_amount = int(people_amount) if people_amount is not None else 1

    try:
        # Calcula a emissão de CO₂
        emission = calculate_emission(
            vehicle=vehicle,
            fuel=fuel,
            people_amount=calculation_people_amount,
            distance=float(distance)
        )

        # Persiste através do serviço
        emission_service.create_record(
            distance=float(distance),
            vehicle=vehicle,
            fuel=fuel,
            people_amount=int(people_amount) if people_amount is not None else None,
            emission_amount=emission
        )

        return jsonify({
            'ok': True,
            'message': f'Emissão calculada: {emission:.2f} kg CO₂.'
        }), 201

    except KeyError as e:
        return jsonify({'ok': False, 'message': f'Combinação inválida de veículo/combustível: {e}'}), 400
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/', methods=['GET'])
def get_emission_record():
    """
    Recupera todos os registros de emissão da base de dados.
    """
    try:
        records = emission_service.get_all_records()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/co2/', methods=['GET'])
def get_co2():
    """
    Calcula e retorna a soma total de CO₂ emitido, lista de emissões e árvores necessárias.
    """
    try:
        summary = emission_service.get_co2_summary()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/vehicles/', methods=['GET'])
def get_vehicles():
    """
    Retorna uma lista de todos os veículos utilizados nos registros.
    """
    try:
        vehicles = emission_service.get_vehicles_summary()
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/fuels/', methods=['GET'])
def get_fuels():
    """
    Retorna uma lista de todos os combustíveis utilizados nos registros.
    """
    try:
        fuels = emission_service.get_fuels_summary()
        return jsonify(fuels), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/km/', methods=['GET'])
def get_km():
    """
    Calcula e retorna a distância total percorrida e a lista de distâncias.
    """
    try:
        km_summary = emission_service.get_km_summary()
        return jsonify(km_summary), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500