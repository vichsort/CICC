"""
Módulo para o registro de emissões de carbono.

Este módulo define uma rota da API para o cálculo e armazenamento de registros de emissão de 
CO₂ provenientes de viagens. Ele lida com a recepção dos dados, o cálculo da emissão 
e a persistência no banco de dados.
"""

from flask import Blueprint, request, jsonify
from backend.database.database import db
from backend.utils.emission_calculator import calculate_emission

emission_record = Blueprint('emission', __name__)

@emission_record.route('/', methods=['POST'])
def create_emission_record():
    """
    Cria e armazena um novo registro de emissão de CO₂.

    Esta rota espera um request do tipo POST com um corpo JSON contendo os
    detalhes da viagem. Com base nesses dados, ela calcula a emissão de CO₂
    correspondente e insere um novo registro na tabela 'emission_records'
    do banco de dados.

    JSON Payload (Corpo da Requisição):
        {
            "person_name": "string",
            "distance": "float",
            "people_amount": "integer | null",
            "vehicle": "string",
            "fuel": "string",
            "vehicle_type": "string | null"
        }

    Returns:
        Response: Um objeto JSON contendo uma mensagem de sucesso e o status HTTP 201 (Created)
                  em caso de sucesso na criação do registro.
    """
    # Extrai os dados do corpo da requisição JSON.
    data = request.json

    # Atribui os valores do JSON a variáveis locais.
    # Usa .get() para evitar erros caso uma chave não exista.
    person_name = data.get('person_name')
    distance = data.get('distance')
    # Define 'None' como padrão para 'people_amount', tornando-o opcional.
    people_amount = data.get('people_amount', None) 
    vehicle = data.get('vehicle')
    fuel = data.get('fuel')

    # Concatena o tipo do veículo ao veículo principal, se existir.
    # Exemplo: 'car' + 'standard' -> 'car-standard'
    if 'vehicle_type' in data:
        vehicle += "-" + str(data.get('vehicle_type'))

    # Chama a função utilitária para calcular a emissão de CO₂.
    # Garante a conversão de tipos para os parâmetros numéricos.
    emission = calculate_emission(
        vehicle=vehicle, 
        fuel=fuel, 
        people_amount=int(people_amount) if people_amount is not None else 1, 
        distance=float(distance)
    )

    # Executa a query para inserir o novo registro no banco de dados.
    # A utilização de parâmetros (%s) previne ataques de SQL Injection.
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
    
    # Retorna uma resposta JSON de sucesso.
    # O status 201 indica que um novo recurso foi criado com sucesso.
    return jsonify(
        {
            'ok': True,
            'message': f'Registro de emissão criado para {person_name}. Emissão calculada: {emission:.2f} kg CO₂.'
        }
    ), 201


@emission_record.route('/', methods=['GET'])
def get_emission_record():
    try:
        records = db.query('SELECT * FROM public.emission_records;')
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500