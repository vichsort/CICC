<script setup>
import { ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import ConsorcioItaForm from './Forms.vue';

const router = useRouter();
const isLoading = ref(false);
const formSubmittedSuccessfully = ref(false);
const apiResponseMessage = ref('');
const emissionValue = ref(null);

let closeTimer = null;

async function handleSubmit(payload) {
  isLoading.value = true;
  apiResponseMessage.value = '';
  emissionValue.value = null;

  try {
    const response = await fetch('http://127.0.0.1:5000/api/emission/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || 'Ocorreu um erro ao enviar os dados.');
    }

    formSubmittedSuccessfully.value = true;
    apiResponseMessage.value = result.message;
    const match = result.message.match(/\d+(\.\d+)?/);

    if (match && match[0]) {
      emissionValue.value = parseFloat(match[0]).toFixed(2);
    } else {
      emissionValue.value = 'N/A';
      console.warn("Não foi possível encontrar um valor numérico na mensagem da API.");
    }
    closeTimer = setTimeout(resetAndRedirect, 10000);

  } catch (error) {
    console.error('Falha na requisição:', error);
    apiResponseMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
}

function resetAndRedirect() {
  formSubmittedSuccessfully.value = false;
  apiResponseMessage.value = '';
  emissionValue.value = null;
  router.push('/');
}

onUnmounted(() => {
  if (closeTimer) {
    clearTimeout(closeTimer);
  }
});
</script>

<template>
  <div class="container">
    <div v-if="formSubmittedSuccessfully" class="modal-overlay">
      <div class="modal-content">
        <p class="confirmation-message">Você emitiu</p>
        <h2 class="emission-value">{{ emissionValue }} kg de CO₂!</h2>
        <p class="confirmation-message light">{{ apiResponseMessage }}</p>

        <div class="progress-bar-container">
          <div class="progress-bar"></div>
        </div>
      </div>
    </div>

    <div v-else>
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Enviando dados...</p>
      </div>

      <ConsorcioItaForm @submit="handleSubmit" v-if="!formSubmittedSuccessfully" />

      <div v-if="apiResponseMessage && !formSubmittedSuccessfully" class="alert alert-danger mt-4">
        <strong>Erro:</strong> {{ apiResponseMessage }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shrink {
  from {
    width: 100%;
  }

  to {
    width: 0%;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background-color: white;
  padding: 3rem 4rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  animation: scaleIn 0.3s ease;
  max-width: 90%;
  width: 600px;
}

.emission-value {
  font-size: 4rem;
  font-weight: 700;
  color: #1e40af;
  margin: 0.5rem 0;
  line-height: 1.1;
}

.confirmation-message {
  font-size: 1.5rem;
  color: #475569;
}

.confirmation-message.light {
  font-size: 1.1rem;
  color: #64748b;
  margin-top: 0.5rem;
}

.progress-bar-container {
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  margin-top: 3rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #3b82f6;
  border-radius: 4px;
  animation: shrink 10s linear forwards;
}

.loading-overlay {
  text-align: center;
  margin-bottom: 2rem;
}

.alert-danger {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
}
</style>