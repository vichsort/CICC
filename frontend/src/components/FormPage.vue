<script setup>
import { ref } from 'vue';
import ConsorcioItaForm from './forms.vue';

const isLoading = ref(false);
const formSubmittedSuccessfully = ref(false);
const apiResponseMessage = ref('');

async function handleSubmit(payload) {
  isLoading.value = true;
  apiResponseMessage.value = '';
  console.log('Enviando para a API:', payload);

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
  } catch (error) {
    console.error('Falha na requisição:', error);
    apiResponseMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
}

function resetForm() {
  formSubmittedSuccessfully.value = false;
  apiResponseMessage.value = '';
}
</script>

<template>
  <main class="container">
    <div v-if="formSubmittedSuccessfully" class="success-screen">
      <h2 class="success-title">✅ Sucesso!</h2>
      <p class="success-message">{{ apiResponseMessage }}</p>
      <button @click="resetForm" class="btn btn-primary btn-lg">Fazer Novo Registro</button>
    </div>

    <div v-else>
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Enviando dados...</p>
      </div>

      <ConsorcioItaForm @submit="handleSubmit" />

      <div v-if="apiResponseMessage" class="alert alert-danger mt-4">
        <strong>Erro:</strong> {{ apiResponseMessage }}
      </div>
    </div>
  </main>
</template>


<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-screen {
  text-align: center;
  padding: 40px;
  background-color: #f0f9f4;
  border-radius: 12px;
  border: 1px solid #d1f0e0;
}

.success-title {
  color: #155724;
  margin-bottom: 1rem;
}

.success-message {
  font-size: 1.2rem;
  margin-bottom: 2rem;
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