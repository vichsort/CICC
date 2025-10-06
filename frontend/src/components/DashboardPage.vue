<script setup>
import { ref, onMounted } from 'vue';
import GraphVeiculos from './GraphVeiculos.vue';
import FuelBarChart from './GraphCombustiveis.vue';
import TreesToCompensate from './TreesToCompensate.vue';

const isLoading = ref(true);
const error = ref(null);
const totalCo2 = ref(0);
const necessaryTrees = ref(0);
const totalKm = ref(0);
const vehicleData = ref({});
const fuelData = ref({});

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function countItems(dataArray, key) { return dataArray.reduce((acc, current) => { const item = current[key]; acc[item] = (acc[item] || 0) + 1; return acc; }, {}); }

async function fetchDashboardData() {
  isLoading.value = true;
  error.value = null;
  try {
    const responses = await Promise.all([
      fetch(`${API_BASE_URL}/co2/`), fetch(`${API_BASE_URL}/km/`),
      fetch(`${API_BASE_URL}/vehicles/`), fetch(`${API_BASE_URL}/fuels/`)
    ]);
    for (const res of responses) { if (!res.ok) { throw new Error('Falha ao buscar um dos recursos da API.'); } }
    const [co2Result, kmResult, vehiclesResult, fuelsResult] = await Promise.all(responses.map(res => res.json()));
    totalCo2.value = parseFloat(co2Result.total_co2).toFixed(2);
    necessaryTrees.value = parseInt(co2Result.necessary_trees);
    totalKm.value = parseFloat(kmResult.total_km).toFixed(2);
    vehicleData.value = countItems(vehiclesResult, 'vehicle');
    fuelData.value = countItems(fuelsResult, 'fuel');
  } catch (err) {
    console.error('Erro ao buscar dados do dashboard:', err);
    error.value = err.message || 'Não foi possível carregar os dados. Tente novamente mais tarde.';
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => { fetchDashboardData(); });
</script>

<template>
  <div class="dashboard-container">
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Carregando dados do dashboard...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      <h4>😕 Ops! Algo deu errado.</h4>
      <p>{{ error }}</p>
      <button @click="fetchDashboardData" class="btn btn-danger">Tentar Novamente</button>
    </div>

    <div v-else class="dashboard-wrapper">
      <h1 class="dashboard-title mb-4">Dashboard de Emissões</h1>

      <div class="row mb-5">
        <div class="col-12">
          <router-link to="/forms" class="btn btn-primary btn-lg new-record-btn">
            ＋ Novo Registro
          </router-link>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-md-6 mb-3 mb-md-0 px-2">
          <div class="card text-center kpi-card minimal-card">
            <div class="card-body">
              <h5 class="card-title">Emissão Total de CO₂</h5>
              <p class="kpi-value">{{ totalCo2 }} kg</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 px-2">
          <div class="card text-center kpi-card minimal-card">
            <div class="card-body">
              <h5 class="card-title">Distância Total Percorrida</h5>
              <p class="kpi-value">{{ totalKm }} km</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-12">
          <div class="card card-trees">
            <TreesToCompensate v-if="Object.keys(vehicleData).length > 0" :data="necessaryTrees" />
            <div v-else class="card-body text-center d-flex align-items-center justify-content-center">
              <p>Nenhum dado de compensação para exibir.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6 mb-3 mb-md-0 px-2">
          <div class="card">
            <div class="card-body">
              <h5 class="chart-title">Veículos Utilizados</h5>
            </div>
            <GraphVeiculos v-if="Object.keys(vehicleData).length > 0" :data="vehicleData" />
            <div v-else class="text-center d-flex align-items-center justify-content-center">
              <p>Nenhum dado de veículo para exibir.</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 px-2">
          <div class="card">
            <div class="card-body">
              <h5 class="chart-title">Combustíveis Utilizados</h5>
            </div>
            <FuelBarChart v-if="Object.keys(fuelData).length > 0" :data="fuelData" />
            <div v-else class="card-body text-center d-flex align-items-center justify-content-center">
              <p>Nenhum dado de combustível para exibir.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #f8f9fa;
}

.dashboard-wrapper {
  width: 100%;
  max-width: 1000px;
}

.dashboard-title {
  color: #333;
  text-align: center;
}

.loading-state {
  text-align: center;
  font-size: 1.2rem;
  color: #555;
}

.kpi-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease-in-out;
}

.kpi-card:hover {
  transform: translateY(-5px);
}

.kpi-card .card-title {
  font-size: 1.1rem;
  color: #6c757d;
  font-weight: 500;
}

.kpi-card .kpi-value {
  font-size: 2.8rem;
  font-weight: 700;
  color: #0d6efd;
  margin-top: 0.5rem;
  margin-bottom: 0;
}

.card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  min-height: 550px;
  box-sizing: border-box;
  display: grid;
  grid-template-rows: auto 1fr;
  overflow: hidden;
}

.chart-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-align: center;
}

.minimal-card {
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-template-rows: unset;
  padding: 0.5rem;
}

.minimal-card .card-body {
  padding: 0.5rem;
  flex-grow: 1;
}

.card-trees {
  min-height: 0px;
}

.new-record-btn {
  width: 100%;
  padding: 1.25rem;
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
  transition: all 0.2s ease-in-out;
}

.new-record-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.4);
}
</style>