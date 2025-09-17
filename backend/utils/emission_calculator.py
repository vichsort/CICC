# Structure of the reference: vehicle -> fuel -> people_amount -> carbon emission
# `None` = amount of people is irrelevant
emission_reference = {
    'micro-bus': {
        'diesel': {
            None: 0.427
        }
    },
    'municipal-bus': {
        'diesel': {
            None: 0.09
        },
        'biodiesel': {
            None: 0.084
        }
    },
    'travel-bus': {
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

def calculate_emission(vehicle, fuel, people_amount, distance):
    return emission_reference[vehicle][fuel][people_amount] * distance
