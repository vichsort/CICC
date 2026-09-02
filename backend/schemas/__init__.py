"""Pacote de schemas de validação Pydantic."""
from backend.schemas.emission_schema import (
    EmissionRecordCreate,
    EmissionRecordResponse,
    EmissionCreateResponse,
    CO2SummaryResponse,
    KMSummaryResponse,
    VehicleItem,
    FuelItem
)

__all__ = [
    'EmissionRecordCreate',
    'EmissionRecordResponse',
    'EmissionCreateResponse',
    'CO2SummaryResponse',
    'KMSummaryResponse',
    'VehicleItem',
    'FuelItem'
]

