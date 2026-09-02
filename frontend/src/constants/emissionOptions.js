/**
 * Constantes e opções de seleção para o formulário de emissões.
 */

export const DISTANCE_RANGES = [
  { text: '0 a 10 km', value: 5 },
  { text: '11 a 15 km', value: 13 },
  { text: '16 a 20 km', value: 18 },
  { text: '21 a 50 km', value: 36 },
  { text: '51 a 80 km', value: 66 },
  { text: '81 a 100 km', value: 91 },
  { text: 'Mais de 100 km', value: 120 },
];

export const VEHICLE_CATEGORIES = [
  { text: 'Carro', value: 'car' },
  { text: 'Motocicleta', value: 'motorcycle' },
  { text: 'Ônibus', value: 'bus' },
];

export const VEHICLE_TYPES = {
  car: [
    { text: 'Gasolina', value: 'standard' },
    { text: 'Flex', value: 'flex' },
    { text: 'Diesel', value: 'diesel' }
  ],
  motorcycle: [
    { text: 'Gasolina', value: 'standard' },
    { text: 'Flex', value: 'flex' }
  ],
  bus: [
    { text: 'Micro-ônibus', value: 'micro-bus' },
    { text: 'Ônibus Municipal', value: 'municipal-bus' },
    { text: 'Ônibus de Viagem', value: 'travel-bus' }
  ]
};

export const FUEL_OPTIONS = {
  car_flex: [
    { text: 'Gasolina', value: 'gasoline' },
    { text: 'Etanol', value: 'ethanol' }
  ],
  motorcycle_flex: [
    { text: 'Gasolina', value: 'gasoline' },
    { text: 'Etanol', value: 'ethanol' }
  ],
};

export const PEOPLE_LIMITS = {
  car: 5,
  motorcycle: 2
};

/**
 * Determina o combustível final com base no tipo de veículo selecionado.
 */
export function resolveFinalFuel(vehicleType, userSelectedFuel) {
  if (vehicleType === 'flex') return userSelectedFuel;
  if (vehicleType === 'standard') return 'gasoline';
  if (vehicleType === 'diesel') return 'diesel';
  if (vehicleType === 'micro-bus') return 'diesel';
  if (vehicleType === 'municipal-bus') return 'biodiesel';
  if (vehicleType === 'travel-bus') return 'diesel';
  return userSelectedFuel;
}

