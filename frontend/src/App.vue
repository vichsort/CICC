<script setup>
import { ref } from 'vue';
import ConsorcioItaForm from './components/ConsorcioItaForm.vue';

// --- Estados Reativos ---
// Controla a exibição do spinner/mensagem de carregamento
const isLoading = ref(false);
// Controla se o formulário foi enviado com sucesso para trocar de tela
const formSubmittedSuccessfully = ref(false);
// Armazena a mensagem de resposta da API (sucesso ou erro)
const apiResponseMessage = ref('');

// --- Função de Envio para a API ---
async function handleSubmit(payload) {
  // 1. Reseta o estado e ativa o "carregando"
  isLoading.value = true;
  apiResponseMessage.value = '';
  console.log('Enviando para a API:', payload);

  try {
    // 2. Monta e executa a requisição POST para a API Flask
    const response = await fetch('http://127.0.0.1:5000/api/emission/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    // Pega o corpo da resposta em formato JSON
    const result = await response.json();

    // 3. Verifica se a requisição foi bem-sucedida (status 2xx)
    if (!response.ok) {
      // Se não foi, lança um erro com a mensagem da API
      throw new Error(result.message || 'Ocorreu um erro ao enviar os dados.');
    }

    // 4. Se foi bem-sucedida, atualiza o estado de sucesso
    formSubmittedSuccessfully.value = true;
    apiResponseMessage.value = result.message; // Exibe a mensagem de sucesso da API

  } catch (error) {
    // 5. Em caso de erro (de rede ou da API), exibe a mensagem de erro
    console.error('Falha na requisição:', error);
    apiResponseMessage.value = error.message;

  } finally {
    // 6. Desativa o "carregando" ao final de tudo
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

<style>
/* Estilos básicos para centralizar e melhorar a aparência */
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

/* Garante que o alerta de erro se destaque */
.alert-danger {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
}
</style>