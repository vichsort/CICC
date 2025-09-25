<template>
  <div class="form-page-wrapper">
    <div class="card shadow-sm large-card">
      <div class="card-body form-section">
        <h3 class="card-title text-center mb-4">Registro de Emissões</h3>

        <form @submit.prevent="onSubmit" novalidate>
          <div class="mb-3">
            <label for="person_name" class="form-label">Nome:</label>
            <input id="person_name" v-model="form.person_name" type="text" class="form-control" required
              aria-required="true" />
            <div v-if="errors.person_name" class="form-text text-danger">{{ errors.person_name }}</div>
          </div>

          <div class="mb-3">
            <label for="distance" class="form-label">Distância (km):</label>
            <input id="distance" v-model="form.distance" type="text" inputmode="decimal" class="form-control"
              required />
            <div v-if="errors.distance" class="form-text text-danger">{{ errors.distance }}</div>
          </div>

          <div class="mb-3">
            <label for="vehicle" class="form-label">Veículo:</label>
            <select id="vehicle" v-model="form.vehicle" class="form-select" required>
              <option value="" disabled>Selecione um veículo</option>
              <option value="bus">Ônibus</option>
              <option value="car">Carro</option>
              <option value="motorcycle">Motocicleta</option>
            </select>
            <div v-if="errors.vehicle" class="form-text text-danger">{{ errors.vehicle }}</div>
          </div>

          <div v-if="showVehicleType" class="mb-3">
            <label for="vehicle_type" class="form-label">Tipo de veículo:</label>
            <select id="vehicle_type" v-model="form.vehicle_type" class="form-select">
              <option value="" disabled>Selecione um tipo</option>
              <option v-for="t in vehicleTypes[form.vehicle]" :key="t.value" :value="t.value">
                {{ t.text }}
              </option>
            </select>
            <div v-if="errors.vehicle_type" class="form-text text-danger">{{ errors.vehicle_type }}</div>
          </div>

          <div v-if="showFuel" class="mb-3">
            <label for="fuel" class="form-label">Combustível:</label>
            <select id="fuel" v-model="form.fuel" class="form-select" :required="showFuel">
              <option value="" disabled>Selecione um combustível</option>
              <option v-for="f in currentFuels" :key="f.value" :value="f.value">
                {{ f.text }}
              </option>
            </select>
            <div v-if="errors.fuel" class="form-text text-danger">{{ errors.fuel }}</div>
          </div>

          <div v-if="showPeopleAmount" class="mb-3">
            <label for="people_amount" class="form-label">Quantas pessoas vieram (incluindo você) neste veículo?</label>
            <input id="people_amount" v-model.number="form.people_amount" type="number" class="form-control"
              :max="peopleMax" min="1" />
            <div v-if="errors.people_amount" class="form-text text-danger">{{ errors.people_amount }}</div>
          </div>

          <div class="d-grid gap-2 mt-4">
            <button type="submit" class="btn btn-primary btn-lg">Enviar</button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from 'vue';

const emit = defineEmits(['submit']);
const peopleLimits = { car: 5, motorcycle: 2 };

const vehicleTypes = {
  car: [
    { text: 'Padrão', value: 'standard' },
    { text: 'Flex', value: 'flex' }
  ],
  motorcycle: [
    { text: 'Padrão', value: 'standard' },
    { text: 'Flex', value: 'flex' }
  ],
  bus: [
    { text: 'Micro-ônibus', value: 'micro-bus' },
    { text: 'Ônibus Municipal', value: 'municipal-bus' },
    { text: 'Ônibus de Viagem', value: 'travel-bus' }
  ]
};

const fuelOptions = {
  car_standard: [
    { text: 'Gasolina', value: 'gasoline' }
  ],
  car_flex: [
    { text: 'Gasolina', value: 'gasoline' },
    { text: 'Etanol', value: 'ethanol' }
  ],
  motorcycle_standard: [
    { text: 'Gasolina', value: 'gasoline' }
  ],
  motorcycle_flex: [
    { text: 'Gasolina', value: 'gasoline' },
    { text: 'Etanol', value: 'ethanol' }
  ],
  'bus_micro-bus': [
    { text: 'Diesel', value: 'diesel' }
  ],
  'bus_municipal-bus': [
    { text: 'Diesel', value: 'diesel' },
    { text: 'Biodiesel', value: 'biodiesel' }
  ],
  'bus_travel-bus': [
    { text: 'Diesel', value: 'diesel' },
    { text: 'Biodiesel', value: 'biodiesel' }
  ]
};

const form = reactive({
  person_name: '',
  distance: '',
  vehicle: '',
  vehicle_type: '',
  fuel: '',
  people_amount: null
});

const errors = reactive({});
const showVehicleType = computed(() => !!form.vehicle);
const showPeopleAmount = computed(() => form.vehicle === 'car' || form.vehicle === 'motorcycle');
const peopleMax = computed(() => peopleLimits[form.vehicle] || null);

const showFuel = computed(() => {
  if (!form.vehicle_type) return false;
  const st = form.vehicle_type;
  if ((form.vehicle !== 'bus' && st === 'standard') || st === 'micro-bus') return false;
  return true;
});

const currentFuels = computed(() => {
  const key = `${form.vehicle}_${form.vehicle_type}`;
  return fuelOptions[key] || [];
});

watch(() => form.vehicle, () => {
  form.vehicle_type = '';
  form.fuel = '';
  form.people_amount = null;
});

watch(() => form.vehicle_type, () => {
  form.fuel = '';
  const fuels = currentFuels.value;
  if (fuels.length === 1 && showFuel.value) {
    form.fuel = fuels[0].value;
  }
});

function normalizeValue(str) {
  if (!str) return '';
  return String(str).toLowerCase().replace(/ /g, '-');
}

function validate() {
  const newErrors = {};

  newErrors.person_name = form.person_name ? '' : 'Nome é obrigatório.';

  const dist = parseFloat(String(form.distance).replace(',', '.'));
  newErrors.distance = (!isNaN(dist) && dist > 0) ? '' : 'Distância deve ser um número positivo.';

  // Validação de Veículo
  newErrors.vehicle = form.vehicle ? '' : 'Selecione um veículo.';

  if (showVehicleType.value) {
    newErrors.vehicle_type = form.vehicle_type ? '' : 'Selecione o tipo de veículo.';
  }

  if (showFuel.value) {
    newErrors.fuel = form.fuel ? '' : 'Selecione o combustível.';
  }

  if (showPeopleAmount.value) {
    newErrors.people_amount = (form.people_amount && form.people_amount >= 1 && form.people_amount <= peopleMax.value)
      ? ''
      : `Quantidade de pessoas (1-${peopleMax.value}) é obrigatória.`;
  }

  for (const key in errors) {
    delete errors[key];
  }

  Object.assign(errors, newErrors);
  return Object.values(newErrors).every(v => v === '');
}

function onSubmit() {
  console.log("Botão clicado, iniciando validação...");

  if (!validate()) {
    console.error("Validação FALHOU!");
    return;
  }

  console.log("Validação passou! Emitindo evento...");

  const distanceNumber = parseFloat(String(form.distance).replace(',', '.'));
  const payload = {
    person_name: form.person_name,
    distance: distanceNumber.toFixed(2),
    vehicle: form.vehicle,
    vehicle_type: form.vehicle_type || null,
    people_amount: showPeopleAmount.value ? form.people_amount : undefined,
    fuel: showFuel.value ? form.fuel : ((form.vehicle !== 'bus' && form.vehicle_type === 'standard') ? 'gasoline' : (form.vehicle_type === 'micro-bus' ? 'diesel' : undefined))
  };
  emit('submit', payload);
}

</script>



<style scoped>
.form-page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
  box-sizing: border-box;
}

.form-section {
  padding: 2.5rem;
}

.large-card {
  width: 60vw;
  max-width: 900px;
  min-width: 360px;
}

.card-title {
  font-size: 1.8rem;
}

.form-control,
.form-select {
  padding: 0.75rem 0.9rem;
  font-size: 1rem;
}

.btn-lg {
  padding: 0.75rem 1rem;
  font-size: 1.05rem;
}
</style>