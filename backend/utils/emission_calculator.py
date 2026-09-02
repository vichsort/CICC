"""
Módulo de cálculo de emissão de CO₂ baseado no tipo de veículo, combustível, passageiros e distância.
Totalmente tipado para análise estrita.
"""

from __future__ import annotations

from typing import Dict, Optional

# Estrutura de referência: vehicle -> fuel -> people_amount -> fator de emissão (kg CO₂/km)
# `None` = quantidade de pessoas irrelevante (ex: ônibus)
emission_reference: Dict[str, Dict[str, Dict[Optional[int], float]]] = {
    'bus-micro-bus': {
        'diesel': {
            None: 0.427
        }
    },
    'bus-municipal-bus': {
        'diesel': {
            None: 0.09
        },
        'biodiesel': {
            None: 0.084
        }
    },
    'bus-travel-bus': {
        'diesel': {
            None: 0.028
        },
        'biodiesel': {
            None: 0.026
        }
    },
    'car-standard': {
        'gasoline': {
            1: 0.135,
            2: 0.068,
            3: 0.045,
            4: 0.034,
            5: 0.027
        },
    },
    'car-flex': {
        'gasoline': {
            1: 0.138,
            2: 0.069,
            3: 0.046,
            4: 0.035,
            5: 0.028
        },
        'ethanol': {
            1: 0.140,
            2: 0.07,
            3: 0.047,
            4: 0.035,
            5: 0.028
        },
    },
    'car-diesel': {
        'diesel': {
            1: 2.5858,
            2: 1.2929,
            3: 0.8619,
            4: 0.6465,
            5: 0.5172
        }
    },
    'motorcycle-standard': {
        'gasoline': {
            1: 0.036,
            2: 0.018
        },
    },
    'motorcycle-flex': {
        'ethanol': {
            1: 0.041,
            2: 0.02
        },
        'gasoline': {
            1: 0.039,
            2: 0.019
        }
    }
}


def calculate_emission(
    vehicle: str,
    fuel: str,
    people_amount: Optional[int],
    distance: float
) -> float:
    """
    Calcula a emissão de CO₂ em kg.

    Args:
        vehicle: Identificador do veículo (ex: 'car-flex', 'bus-municipal-bus').
        fuel: Tipo do combustível (ex: 'gasoline', 'ethanol', 'diesel').
        people_amount: Número de passageiros (ou None para ônibus).
        distance: Distância percorrida em quilômetros.

    Returns:
        float: Emissão calculada em kg CO₂.
    """
    factor: float = emission_reference[vehicle][fuel][people_amount]
    return float(factor * distance)
