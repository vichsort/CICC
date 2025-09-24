"""
Módulo para o registro de emissões de carbono.

Este módulo define rotas de uma API Flask para o cálculo, armazenamento e consulta
de registros de emissão de CO₂ provenientes de viagens.
"""
from decimal import Decimal
from flask import Blueprint, request, jsonify
from backend.database.database import db
from backend.utils.emission_calculator import calculate_emission

# Cria um Blueprint do Flask para organizar as rotas de emissão.
# O prefixo da URL para estas rotas será definido no app principal.
emission_record = Blueprint('emission', __name__)

@emission_record.route('/', methods=['POST'])
def create_emission_record():
    """
    Cria e armazena um novo registro de emissão de CO₂.

    Esta rota espera uma requisição POST com um corpo JSON contendo os
    detalhes da viagem. Com base nesses dados, ela calcula a emissão de CO₂
    correspondente e insere um novo registro na tabela 'emission_records'.

    JSON Payload (Corpo da Requisição):
        {
            "person_name": "string",
            "distance": "float",
            "vehicle": "string",
            "vehicle_type": "string | null",
            "fuel": "string",
            "people_amount": "integer | null"
        }

    Returns:
        Response: Em caso de sucesso, retorna um objeto JSON com uma mensagem
                  e o status HTTP 201 (Created).
        Exemplo de Sucesso (201):
        {
            "ok": true,
            "message": "Registro de emissão criado para João. Emissão calculada: 15.75 kg CO₂."
        }
    """
    data = request.json

    person_name = data.get('person_name')
    distance = data.get('distance')
    people_amount = data.get('people_amount', None)
    vehicle = data.get('vehicle')
    fuel = data.get('fuel')
    vehicle_type = data.get('vehicle_type')

    # Concatena o tipo do veículo ao veículo principal, se existir.
    # Exemplo: 'car' + 'standard' -> 'car-standard'
    if vehicle_type:
        vehicle += "-" + str(vehicle_type)

    # Para o cálculo, se não for um ônibus, considera pelo menos 1 pessoa.
    calculation_people_amount = None
    if 'bus' not in vehicle:
        calculation_people_amount = int(people_amount) if people_amount is not None else 1

    # Chama a função utilitária para calcular a emissão de CO₂.
    emission = calculate_emission(
        vehicle=vehicle,
        fuel=fuel,
        people_amount=calculation_people_amount,
        distance=float(distance)
    )

    # Executa a query para inserir o novo registro no banco de dados.
    # O uso de parâmetros (%s) previne ataques de SQL Injection.
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

    # Retorna uma resposta JSON de sucesso com status 201.
    return jsonify({
        'ok': True,
        'message': f'Registro de emissão criado para {person_name}. Emissão calculada: {emission:.2f} kg CO₂.'
    }), 201


@emission_record.route('/', methods=['GET'])
def get_emission_record():
    """
    Recupera todos os registros de emissão da base de dados.

    Returns:
        Response: Um JSON contendo uma lista de todos os registros de emissão
                  ou uma mensagem de erro.
    
    Exemplo de Sucesso (200):
        [
            {
                "id": 1,
                "person_name": "João Silva",
                "emission_amount": "15.75",
                "distance": "100.00",
                "people_amount": 1,
                "vehicle": "car-flex",
                "fuel": "gasoline",
                "created_at": "2025-09-24T18:30:00Z"
            }
        ]
    
    Exemplo de Erro (500):
        {
            "ok": false,
            "message": "Descrição do erro do banco de dados."
        }
    """
    try:
        records = db.query('SELECT * FROM public.emission_records;')
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/co2/', methods=['GET'])
def get_co2():
    """
    Calcula e retorna a soma total de CO₂ emitido e a lista de emissões individuais.

    Returns:
        Response: Um JSON com o total de CO₂ e uma lista de cada registro de emissão.
    
    Exemplo de Sucesso (200):
        {
            "total_co2": "120.50",
            "records": [
                { "emission_amount": "15.75" },
                { "emission_amount": "104.75" }
            ]
        }
        
    Exemplo de Erro (500):
        {
            "ok": false,
            "message": "Descrição do erro."
        }
    """
    try:
        co2_records = db.query('SELECT emission_amount FROM public.emission_records;')
        total_co2 = sum(Decimal(record['emission_amount']) for record in co2_records)

        return jsonify({
            'total_co2': str(total_co2),
            'records': co2_records
        }), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/vehicles/', methods=['GET'])
def get_vehicles():
    """
    Retorna uma lista de todos os veículos utilizados nos registros.

    Returns:
        Response: Um JSON contendo uma lista de objetos, cada um com a chave 'vehicle'.
    
    Exemplo de Sucesso (200):
        [
            { "vehicle": "car-flex" },
            { "vehicle": "bus-municipal-bus" }
        ]
        
    Exemplo de Erro (500):
        {
            "ok": false,
            "message": "Descrição do erro."
        }
    """
    try:
        vehicles = db.query('SELECT vehicle FROM public.emission_records;')
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/fuels/', methods=['GET'])
def get_fuels():
    """
    Retorna uma lista de todos os combustíveis utilizados nos registros.

    Returns:
        Response: Um JSON contendo uma lista de objetos, cada um com a chave 'fuel'.
        
    Exemplo de Sucesso (200):
        [
            { "fuel": "gasoline" },
            { "fuel": "diesel" }
        ]
        
    Exemplo de Erro (500):
        {
            "ok": false,
            "message": "Descrição do erro."
        }
    """
    try:
        fuels = db.query('SELECT fuel FROM public.emission_records;')
        return jsonify(fuels), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/km/', methods=['GET'])
def get_km():
    """
    Calcula e retorna a distância total percorrida e a lista de distâncias individuais.

    Returns:
        Response: Um JSON com o total de KM e uma lista de cada registro de distância.
    
    Exemplo de Sucesso (200):
        {
            "total_km": "250.50",
            "records": [
                { "distance": "100.00" },
                { "distance": "150.50" }
            ]
        }
        
    Exemplo de Erro (500):
        {
            "ok": false,
            "message": "Descrição do erro."
        }
    """
    try:
        km_records = db.query('SELECT distance FROM public.emission_records;')
        total_km = sum(Decimal(record['distance']) for record in km_records)

        return jsonify({
            'total_km': str(total_km),
            'records': km_records
        }), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500