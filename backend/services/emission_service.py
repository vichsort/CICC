"""
Camada de serviço para gerenciamento e regras de negócio de emissões de carbono.

Totalmente tipado para checagem estrita de tipos (Pylance/Pyright/Mypy/Pydantic).
"""

from __future__ import annotations

from decimal import Decimal
from math import ceil
from typing import Any, Dict, List, Optional
from backend.database.database import db


class EmissionService:
    """
    Serviço que encapsula a lógica de persistência e consulta de emissões.
    """

    def create_record(
        self,
        distance: float,
        vehicle: str,
        fuel: str,
        people_amount: Optional[int],
        emission_amount: float
    ) -> int:
        """
        Insere um novo registro de emissão no banco de dados.

        Returns:
            int: Quantidade de linhas afetadas.
        """
        return db.execute(
            "INSERT INTO emission_records "
            "(emission_amount, distance, people_amount, vehicle, fuel) "
            "VALUES (%s, %s, %s, %s, %s);",
            (
                round(float(emission_amount), 4),
                round(float(distance), 2),
                people_amount,
                vehicle,
                fuel
            )
        )

    def get_all_records(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os registros de emissão cadastrados.
        """
        records: List[Dict[str, Any]] = db.query("SELECT * FROM emission_records ORDER BY id_record ASC;")
        return self._normalize_records(records)

    def get_co2_summary(self) -> Dict[str, Any]:
        """
        Calcula o total de CO₂ emitido, a lista de emissões e a estimativa
        de árvores necessárias para compensação.
        """
        records: List[Dict[str, Any]] = db.query("SELECT emission_amount FROM emission_records;")
        
        total_co2: Decimal = Decimal('0')
        normalized_records: List[Dict[str, str]] = []

        for record in records:
            amount: Decimal = Decimal(str(record.get('emission_amount', 0)))
            total_co2 += amount
            normalized_records.append({'emission_amount': str(amount)})

        # Regra de negócio: 7 árvores por tonelada de CO2 emitido
        trees_per_ton: int = 7
        necessary_trees: int = ceil((total_co2 * Decimal(trees_per_ton)) / Decimal(1000))

        return {
            'records': normalized_records,
            'total_co2': str(total_co2),
            'necessary_trees': necessary_trees
        }

    def get_vehicles_summary(self) -> List[Dict[str, Any]]:
        """
        Retorna a lista de veículos registrados.
        """
        return db.query("SELECT vehicle FROM emission_records;")

    def get_fuels_summary(self) -> List[Dict[str, Any]]:
        """
        Retorna a lista de combustíveis registrados.
        """
        return db.query("SELECT fuel FROM emission_records;")

    def get_km_summary(self) -> Dict[str, Any]:
        """
        Calcula a distância total percorrida e a lista de distâncias registradas.
        """
        records: List[Dict[str, Any]] = db.query("SELECT distance FROM emission_records;")
        
        total_km: Decimal = Decimal('0')
        normalized_records: List[Dict[str, str]] = []

        for record in records:
            dist: Decimal = Decimal(str(record.get('distance', 0)))
            total_km += dist
            normalized_records.append({'distance': str(dist)})

        return {
            'total_km': str(total_km),
            'records': normalized_records
        }

    def get_export_records(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os registros formatados para exportação (CSV / Excel).
        """
        records: List[Dict[str, Any]] = db.query("""
            SELECT 
                id_record,
                emission_amount,
                distance,
                people_amount,
                vehicle,
                fuel,
                created_at
            FROM emission_records 
            ORDER BY id_record ASC;
        """)
        return self._normalize_records(records)

    def _normalize_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normaliza os tipos de dados (ex: Decimal, float, datas) para garantir
        compatibilidade total com serialização JSON e exportação.
        """
        normalized: List[Dict[str, Any]] = []
        for r in records:
            item: Dict[str, Any] = dict(r)
            if 'emission_amount' in item and item['emission_amount'] is not None:
                item['emission_amount'] = str(item['emission_amount'])
            if 'distance' in item and item['distance'] is not None:
                item['distance'] = str(item['distance'])
            if 'created_at' in item and item['created_at'] is not None:
                item['created_at'] = str(item['created_at'])
            normalized.append(item)
        return normalized


# Instância única do serviço
emission_service: EmissionService = EmissionService()
