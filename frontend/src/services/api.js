/**
 * Camada de serviço de API para comunicação HTTP com o backend Flask.
 */

const API_BASE = '/api/emission';

/**
 * Função auxiliar para contar a frequência de itens em uma lista de objetos.
 * Ex: [{ vehicle: 'car' }, { vehicle: 'bus' }, { vehicle: 'car' }] -> { car: 2, bus: 1 }
 */
function countOccurrences(dataArray, key) {
  return dataArray.reduce((acc, current) => {
    const item = current[key];
    if (item) {
      acc[item] = (acc[item] || 0) + 1;
    }
    return acc;
  }, {});
}

export const emissionApi = {
  /**
   * Busca todos os dados consolidados do dashboard em paralelo.
   */
  async getDashboardSummary() {
    const responses = await Promise.all([
      fetch(`${API_BASE}/co2/`),
      fetch(`${API_BASE}/km/`),
      fetch(`${API_BASE}/vehicles/`),
      fetch(`${API_BASE}/fuels/`)
    ]);

    for (const res of responses) {
      if (!res.ok) {
        throw new Error('Falha ao buscar os recursos do dashboard.');
      }
    }

    const [co2Result, kmResult, vehiclesResult, fuelsResult] = await Promise.all(
      responses.map(res => res.json())
    );

    return {
      totalCo2: parseFloat(co2Result.total_co2).toFixed(2),
      necessaryTrees: parseInt(co2Result.necessary_trees, 10),
      totalKm: parseFloat(kmResult.total_km).toFixed(2),
      vehicleData: countOccurrences(vehiclesResult, 'vehicle'),
      fuelData: countOccurrences(fuelsResult, 'fuel')
    };
  },

  /**
   * Envia os dados de uma nova viagem para cálculo e persistência.
   */
  async createEmission(payload) {
    const response = await fetch(`${API_BASE}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Ocorreu um erro ao enviar os dados.');
    }

    return data;
  },

  /**
   * Verifica se o PIN administrativo informado está correto.
   */
  async verifyAdminPin(pin) {
    const response = await fetch(`${API_BASE}/verify-pin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin: pin.trim() })
    });

    const data = await response.json();

    if (!response.ok || !data.ok) {
      throw new Error(data.message || 'PIN incorreto.');
    }

    return data;
  },

  /**
   * Retorna a URL de download direto do relatório CSV.
   */
  getExportUrl(pin) {
    return `${API_BASE}/export?pin=${encodeURIComponent(pin.trim())}`;
  }
};

