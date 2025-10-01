const vehicleTypeTranslations = {
  'motorcycle-flex': 'Motocicleta Flex',
  'motorcycle-standard': 'Motocicleta à Gasolina',
  'car-flex': 'Carro Flex',
  'car-diesel': 'Carro à Diesel',
  'car-standard': 'Carro à Gasolina',
  'bus-municipal-bus': 'Ônibus Municipal',
  'bus-micro-bus': 'Micro-ônibus',
  'bus-travel-bus': 'Ônibus de Viagem',
  
  'car': 'Carro',
  'bus': 'Ônibus',
  'motorcycle': 'Motocicleta',

  'gasoline': 'Gasolina',
  'ethanol': 'Etanol',
  'diesel': 'Diesel',
  'biodiesel': 'Biodiesel'
};

/**
 * Traduz uma chave de veículo/tipo/combustível de inglês para português.
 * Se a chave não for encontrada, retorna a própria chave (mantém o original).
 * @param {string} key A chave a ser traduzida (ex: 'car-flex', 'bus', 'gasoline').
 * @returns {string} A tradução em português ou a chave original.
 */
export function translateVehicleKey(key) {
  return vehicleTypeTranslations[key] || key;
}