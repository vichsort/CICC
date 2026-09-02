"""
Módulo para o registro e exportação de emissões de carbono.

Este módulo define rotas da API Flask com validação estrita via Pydantic,
persistência através do emission_service e exportação protegida por PIN.
"""

from __future__ import annotations

import csv
import io
import os
from datetime import date
from typing import Any, Dict, List, Optional, Tuple, Union
from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from backend.schemas.emission_schema import EmissionRecordCreate
from backend.services.emission_service import emission_service
from backend.utils.emission_calculator import calculate_emission

# Cria um Blueprint do Flask para organizar as rotas de emissão.
emission_record: Blueprint = Blueprint('emission', __name__)


def _is_valid_pin(provided_pin: Optional[str]) -> bool:
    """Verifica se o PIN informado confere com o configurado nas variáveis de ambiente."""
    expected_pin: str = os.environ.get('ADMIN_PIN', '1234').strip()
    return bool(provided_pin and str(provided_pin).strip() == expected_pin)


@emission_record.route('/', methods=['POST'])
def create_emission_record() -> Tuple[Response, int]:
    """
    Cria e armazena um novo registro de emissão de CO₂.
    """
    raw_data: Dict[str, Any] = request.get_json(silent=True) or {}

    try:
        payload: EmissionRecordCreate = EmissionRecordCreate.model_validate(raw_data)
        distance: float = payload.distance
        vehicle: str = payload.get_full_vehicle()
        fuel: str = payload.fuel
        people_amount: Optional[int] = payload.people_amount
    except ValidationError as err:
        return jsonify({'ok': False, 'message': 'Dados inválidos.', 'errors': err.errors()}), 400

    # Para o cálculo, se não for um ônibus, considera pelo menos 1 pessoa.
    calc_people: Optional[int] = None if 'bus' in vehicle else (people_amount or 1)

    try:
        emission: float = calculate_emission(
            vehicle=vehicle,
            fuel=fuel,
            people_amount=calc_people,
            distance=distance
        )

        emission_service.create_record(
            distance=distance,
            vehicle=vehicle,
            fuel=fuel,
            people_amount=people_amount,
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
def get_emission_record() -> Tuple[Response, int]:
    """
    Recupera todos os registros de emissão da base de dados.
    """
    try:
        records: List[Dict[str, Any]] = emission_service.get_all_records()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/co2/', methods=['GET'])
def get_co2() -> Tuple[Response, int]:
    """
    Calcula e retorna a soma total de CO₂ emitido, lista de emissões e árvores necessárias.
    """
    try:
        summary: Dict[str, Any] = emission_service.get_co2_summary()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/vehicles/', methods=['GET'])
def get_vehicles() -> Tuple[Response, int]:
    """
    Retorna uma lista de todos os veículos utilizados nos registros.
    """
    try:
        vehicles: List[Dict[str, Any]] = emission_service.get_vehicles_summary()
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/fuels/', methods=['GET'])
def get_fuels() -> Tuple[Response, int]:
    """
    Retorna uma lista de todos os combustíveis utilizados nos registros.
    """
    try:
        fuels: List[Dict[str, Any]] = emission_service.get_fuels_summary()
        return jsonify(fuels), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/km/', methods=['GET'])
def get_km() -> Tuple[Response, int]:
    """
    Calcula e retorna a distância total percorrida e a lista de distâncias.
    """
    try:
        km_summary: Dict[str, Any] = emission_service.get_km_summary()
        return jsonify(km_summary), 200
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 500


@emission_record.route('/verify-pin', methods=['POST'])
def verify_pin() -> Tuple[Response, int]:
    """
    Valida se o PIN administrativo fornecido está correto.
    """
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    pin: Optional[str] = data.get('pin')

    if _is_valid_pin(pin):
        return jsonify({'ok': True, 'message': 'PIN validado com sucesso.'}), 200
    return jsonify({'ok': False, 'message': 'PIN incorreto.'}), 401


@emission_record.route('/export', methods=['GET'])
def export_csv() -> Union[Response, Tuple[Response, int]]:
    """
    Gera e envia o download do arquivo CSV com todos os registros, protegido por PIN.
    O PIN pode ser passado como query param (?pin=...) ou no header X-Admin-Pin.
    """
    pin: Optional[str] = request.args.get('pin') or request.headers.get('X-Admin-Pin')

    if not _is_valid_pin(pin):
        return jsonify({'ok': False, 'message': 'Não autorizado. PIN inválido ou ausente.'}), 401

    try:
        records: List[Dict[str, Any]] = emission_service.get_export_records()

        # Monta o CSV em memória
        output: io.StringIO = io.StringIO()
        # Escreve o BOM UTF-8 para garantir abertura correta no Excel do Windows
        output.write('\ufeff')
        
        writer = csv.writer(output, delimiter=';')
        writer.writerow([
            'ID',
            'Emissão (kg CO₂)',
            'Distância (km)',
            'Passageiros',
            'Veículo',
            'Combustível',
            'Data e Hora'
        ])

        for r in records:
            writer.writerow([
                r.get('id_record', ''),
                str(r.get('emission_amount', '')).replace('.', ','),
                str(r.get('distance', '')).replace('.', ','),
                r.get('people_amount') if r.get('people_amount') is not None else 'Ind.',
                r.get('vehicle', ''),
                r.get('fuel', ''),
                r.get('created_at', '')
            ])

        csv_content: str = output.getvalue()
        today_str: str = date.today().strftime('%Y-%m-%d')
        filename: str = f"emissions_{today_str}.csv"

        return Response(
            csv_content,
            mimetype="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache"
            }
        )

    except Exception as e:
        return jsonify({'ok': False, 'message': f'Erro ao gerar CSV: {e}'}), 500