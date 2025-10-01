<template>
  <div class="form-page-wrapper">
    <div class="card shadow-sm large-card">
      <div class="card-body form-section">
        <h3 class="card-title text-center mb-5">Registro de Emissões</h3>

        <form @submit.prevent="onSubmit" novalidate>
          <div class="mb-4">
            <label class="form-label">Distância percorrida (km):</label>
            <div class="choice-group">
               <button
                  type="button"
                  v-for="dist in distanceRanges"
                  :key="dist.value"
                  class="choice-btn"
                  :class="{ 'selected': form.distance === dist.value }"
                  @click="form.distance = dist.value"
               >
                  {{ dist.text }}
               </button>
            </div>
            <div v-if="errors.distance" class="form-text text-danger">{{ errors.distance }}</div>
          </div>

          <div class="mb-4">
            <label class="form-label">Qual o seu veículo?</label>
            <div class="choice-group">
              <button
                type="button"
                v-for="cat in vehicleCategories"
                :key="cat.value"
                class="choice-btn"
                :class="{ 'selected': form.vehicle === cat.value }"
                @click="selectVehicle(cat.value)"
              >
                {{ cat.text }}
              </button>
            </div>
            <div v-if="errors.vehicle" class="form-text text-danger">{{ errors.vehicle }}</div>
          </div>

          <div v-if="form.vehicle" class="mb-4 animated-section">
            <label class="form-label">Qual o tipo de {{ selectedVehicleText.toLowerCase() }}?</label>
            <div class="choice-group">
              <button
                type="button"
                v-for="type in vehicleTypes[form.vehicle]"
                :key="type.value"
                class="choice-btn"
                :class="{ 'selected': form.vehicle_type === type.value }"
                @click="selectVehicleType(type.value)"
              >
                {{ type.text }}
              </button>
            </div>
             <div v-if="errors.vehicle_type" class="form-text text-danger">{{ errors.vehicle_type }}</div>
          </div>
          
          <div v-if="showFuel" class="mb-4 animated-section">
            <label class="form-label">Qual o combustível?</label>
            <div class="choice-group">
              <button
                type="button"
                v-for="fuel in currentFuels"
                :key="fuel.value"
                class="choice-btn"
                :class="{ 'selected': form.fuel === fuel.value }"
                @click="form.fuel = fuel.value"
              >
                {{ fuel.text }}
              </button>
            </div>
            <div v-if="errors.fuel" class="form-text text-danger">{{ errors.fuel }}</div>
          </div>

          <div v-if="showPeopleAmount" class="mb-4 animated-section">
            <label class="form-label">Quantas pessoas no veículo (incluindo você)?</label>
            <div class="choice-group">
              <button
                type="button"
                v-for="n in peopleMax"
                :key="n"
                class="choice-btn" :class="{ 'selected': form.people_amount === n }"
                @click="form.people_amount = n"
              >
                {{ n }}
              </button>
            </div>
            <div v-if="errors.people_amount" class="form-text text-danger">{{ errors.people_amount }}</div>
          </div>
          <div class="d-grid gap-2 mt-5">
            <button type="submit" class="btn btn-primary btn-lg">Registrar Emissão</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue';

const emit = defineEmits(['submit']);
const peopleLimits = { car: 5, motorcycle: 2 };

const distanceRanges = [
  { text: '0 a 10 km', value: 5 },
  { text: '11 a 15 km', value: 13 },
  { text: '16 a 20 km', value: 18 },
  { text: '21 a 50 km', value: 36 },
  { text: '51 a 80 km', value: 66 },
  { text: '81 a 100 km', value: 91 },
  { text: 'Mais de 100 km', value: 120 },
];

const vehicleCategories = [
  { text: 'Carro', value: 'car' },
  { text: 'Motocicleta', value: 'motorcycle' },
  { text: 'Ônibus', value: 'bus' },
];

const vehicleTypes = {
  car: [ { text: 'Gasolina', value: 'standard' }, { text: 'Flex', value: 'flex' }, { text: 'Diesel', value: 'diesel' } ],
  motorcycle: [ { text: 'Gasolina', value: 'standard' }, { text: 'Flex', value: 'flex' } ],
  bus: [ { text: 'Micro-ônibus', value: 'micro-bus' }, { text: 'Ônibus Municipal', value: 'municipal-bus' }, { text: 'Ônibus de Viagem', value: 'travel-bus' } ]
};

const fuelOptions = {
  car_flex: [{ text: 'Gasolina', value: 'gasoline' }, { text: 'Etanol', value: 'ethanol' }],
  motorcycle_flex: [{ text: 'Gasolina', value: 'gasoline' }, { text: 'Etanol', value: 'ethanol' }],
};

const form = reactive({
  distance: '', vehicle: '', vehicle_type: '', fuel: '', people_amount: null
});

const errors = reactive({});

function selectVehicle(vehicle) {
  form.vehicle = vehicle;
  form.vehicle_type = '';
  form.fuel = '';
  form.people_amount = null;
}

function selectVehicleType(type) {
  form.vehicle_type = type;
  form.fuel = '';
}

const selectedVehicleText = computed(() => {
  return vehicleCategories.find(cat => cat.value === form.vehicle)?.text || '';
});

const showPeopleAmount = computed(() => form.vehicle === 'car' || form.vehicle === 'motorcycle');
const peopleMax = computed(() => peopleLimits[form.vehicle] || null);
const showFuel = computed(() => form.vehicle_type === 'flex');
const currentFuels = computed(() => {
  const key = `${form.vehicle}_${form.vehicle_type}`;
  return fuelOptions[key] || [];
});

function getFinalFuel() {
    if (form.vehicle_type === 'flex') return form.fuel;
    if (form.vehicle_type === 'standard') return 'gasoline';
    if (form.vehicle_type === 'diesel') return 'diesel';
    if (form.vehicle_type === 'micro-bus') return 'diesel';
    if (form.vehicle_type === 'municipal-bus') return 'biodiesel';
    if (form.vehicle_type === 'travel-bus') return 'diesel';
    return form.fuel; 
}


function validate() {
  Object.keys(errors).forEach(key => delete errors[key]);
  const newErrors = {};
  if (!form.distance) newErrors.distance = 'Selecione uma faixa de distância.';
  if (!form.vehicle) newErrors.vehicle = 'Selecione um veículo.';
  if (form.vehicle && !form.vehicle_type) newErrors.vehicle_type = 'Selecione um tipo de veículo.';
  if (showFuel.value && !form.fuel) newErrors.fuel = 'Selecione um combustível.';
  if (showPeopleAmount.value && !form.people_amount) newErrors.people_amount = 'Informe a quantidade de pessoas.';
  Object.assign(errors, newErrors);
  return Object.keys(newErrors).length === 0;
}


function onSubmit() {
  if (!validate()) {
    console.error("Validação FALHOU!", errors);
    return;
  }

  const finalFuel = getFinalFuel();

  const payload = {
    distance: form.distance,
    vehicle: `${form.vehicle}-${form.vehicle_type}`,
    people_amount: showPeopleAmount.value ? form.people_amount : null,
    fuel: finalFuel,
  };

  emit('submit', payload);
}
</script>

<style scoped>
.form-page-wrapper { display: flex; justify-content: center; align-items: center; padding: 2rem; box-sizing: border-box; width: 100%; }
.form-section { padding: 3rem; }
.large-card { width: clamp(480px, 75vw, 1600px); }
.card-title { font-size: 2rem; font-weight: 600; color: #334155; }
.form-label { font-weight: 500; font-size: 1.1rem; color: #475569; margin-bottom: 0.75rem; }
.form-control { padding: 0.75rem 1rem; font-size: 1rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; }
.btn-lg { padding: 1rem 1.5rem; font-size: 1.1rem; font-weight: 600; border-radius: 0.5rem; }

.choice-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.choice-btn {
  flex-grow: 1;
  padding: 1.25rem;
  font-size: 1.1rem;
  font-weight: 500;
  text-align: center;
  background-color: #ffffff;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  color: #334155;
}

.choice-btn:hover {
  border-color: #93c5fd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.choice-btn.selected {
  background-color: #eff6ff;
  border-color: #3b82f6;
  color: #2563eb;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animated-section {
  animation: fadeIn 0.4s ease-in-out;
}
</style>