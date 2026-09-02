"""
Schemas Pydantic para validação estrita de dados de entrada e saída da API.
"""

from __future__ import annotations

from typing import Any, List, Optional
from pydantic import BaseModel, Field, field_validator


class EmissionRecordCreate(BaseModel):
    """Schema para validação do payload de criação de novo registro de emissão."""
    distance: float = Field(..., gt=0, description="Distância percorrida em quilômetros")
    vehicle: str = Field(..., min_length=1, description="Categoria do veículo (ex: 'car', 'bus', 'motorcycle')")
    fuel: str = Field(..., min_length=1, description="Combustível utilizado (ex: 'gasoline', 'ethanol', 'diesel')")
    people_amount: Optional[int] = Field(default=None, ge=1, le=10, description="Quantidade de pessoas no veículo")
    vehicle_type: Optional[str] = Field(default=None, description="Subtipo ou modelo do veículo")

    @field_validator('distance', mode='before')
    @classmethod
    def parse_distance(cls, value: Any) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError("A distância deve ser um número válido.")

    @field_validator('people_amount', mode='before')
    @classmethod
    def parse_people_amount(cls, value: Any) -> Optional[int]:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError("A quantidade de pessoas deve ser um número inteiro.")

    def get_full_vehicle(self) -> str:
        """Retorna o identificador completo do veículo (ex: 'car-flex')."""
        if self.vehicle_type:
            return f"{self.vehicle}-{self.vehicle_type}"
        return self.vehicle


class EmissionRecordResponse(BaseModel):
    """Schema de um registro de emissão recuperado do banco."""
    id_record: int
    emission_amount: str
    distance: str
    people_amount: Optional[int] = None
    vehicle: str
    fuel: str
    created_at: Optional[str] = None


class EmissionCreateResponse(BaseModel):
    """Resposta de sucesso da criação de registro."""
    ok: bool = True
    message: str


class CO2SummaryItem(BaseModel):
    emission_amount: str


class CO2SummaryResponse(BaseModel):
    """Resposta do resumo de CO₂ e árvores."""
    records: List[CO2SummaryItem]
    total_co2: str
    necessary_trees: int


class KMSummaryItem(BaseModel):
    distance: str


class KMSummaryResponse(BaseModel):
    """Resposta do resumo de quilometragem."""
    records: List[KMSummaryItem]
    total_km: str


class VehicleItem(BaseModel):
    vehicle: str


class FuelItem(BaseModel):
    fuel: str

