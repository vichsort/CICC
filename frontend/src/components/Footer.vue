<script setup>
import { ref } from 'vue';
import { emissionApi } from '../services/api';

const developers = ref([
    'Gabriel Moura Jappe',
    'Gustavo Schwitzki Peretti',
    'Vitor Marcelo Mignoni',
    'Heitor Scalco Neto'
]);

const currentYear = new Date().getFullYear();

// --- Lógica do Painel Administrativo Oculto (5 Cliques) ---
const clickCount = ref(0);
let clickTimeout = null;

const showAdminModal = ref(false);
const adminPin = ref('');
const isVerifying = ref(false);
const pinError = ref('');
const isAuthorized = ref(false);

function handleLogoClick() {
    clickCount.value++;
    if (clickTimeout) {
        clearTimeout(clickTimeout);
    }

    if (clickCount.value >= 5) {
        clickCount.value = 0;
        openAdminModal();
    } else {
        clickTimeout = setTimeout(() => {
            clickCount.value = 0;
        }, 2500); // 5 cliques em até 2.5 segundos
    }
}

function openAdminModal() {
    showAdminModal.value = true;
    adminPin.value = '';
    pinError.value = '';
    isAuthorized.value = false;
}

function closeAdminModal() {
    showAdminModal.value = false;
    adminPin.value = '';
    pinError.value = '';
    isAuthorized.value = false;
}

async function verifyPin() {
    if (!adminPin.value.trim()) {
        pinError.value = 'Por favor, digite o PIN.';
        return;
    }

    isVerifying.value = true;
    pinError.value = '';

    try {
        await emissionApi.verifyAdminPin(adminPin.value.trim());
        isAuthorized.value = true;
    } catch (err) {
        pinError.value = err.message || 'PIN incorreto ou falha na conexão.';
    } finally {
        isVerifying.value = false;
    }
}

function downloadCsv() {
    const downloadUrl = emissionApi.getExportUrl(adminPin.value.trim());
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', '');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
</script>

<template>
    <footer class="app-footer">
        <div class="footer-container">
            <div class="footer-section logos-section">
                <h4 class="footer-title">Realização</h4>
                <div class="logo-wrapper">
                    <!-- Logo com detector de 5 cliques rápidos -->
                    <div 
                        class="logo-placeholder clickable-logo" 
                        @click="handleLogoClick"
                        title="Consórcio Itá"
                    >
                        <img src="../assets/ita.png" alt="Consórcio Itá">
                        <p>Consórcio Itá</p>
                    </div>

                    <div class="logo-placeholder">
                        <img src="../assets/ifc_white.png" alt="Instituto Federal Catarinense">
                        <p>Instituto Federal Catarinense</p>
                    </div>
                </div>
            </div>

            <div class="footer-section devs-section">
                <h4 class="footer-title">Desenvolvedores</h4>
                <ul class="dev-list">
                    <li v-for="dev in developers" :key="dev">{{ dev }}</li>
                </ul>
            </div>
        </div>

        <div class="footer-copyright">
            <p>&copy; {{ currentYear }} Todos os direitos reservados.</p>
        </div>

        <!-- Modal Administrativo de Exportação -->
        <div v-if="showAdminModal" class="admin-modal-overlay" @click.self="closeAdminModal">
            <div class="admin-modal-card">
                <div class="admin-modal-header">
                    <h3>🔐 Administração do Totem</h3>
                    <button class="btn-close-custom" @click="closeAdminModal">&times;</button>
                </div>

                <div class="admin-modal-body">
                    <!-- Estado 1: Solicitação de PIN -->
                    <div v-if="!isAuthorized">
                        <p class="text-muted mb-3">Digite o PIN de administrador para acessar os dados e exportações:</p>
                        
                        <form @submit.prevent="verifyPin">
                            <div class="mb-3">
                                <input 
                                    type="password" 
                                    v-model="adminPin" 
                                    class="form-control form-control-lg text-center pin-input" 
                                    placeholder="Digite o PIN" 
                                    maxlength="20"
                                    autofocus
                                />
                            </div>

                            <div v-if="pinError" class="alert alert-danger py-2 mb-3">
                                {{ pinError }}
                            </div>

                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary btn-lg" :disabled="isVerifying">
                                    <span v-if="isVerifying" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ isVerifying ? 'Verificando...' : 'Acessar' }}
                                </button>
                            </div>
                        </form>
                    </div>

                    <!-- Estado 2: Autenticado com sucesso -->
                    <div v-else class="text-center py-2">
                        <div class="auth-success-badge mb-3">
                            <span class="fs-1">✅</span>
                            <h5 class="mt-2 text-success">Autenticado com Sucesso!</h5>
                        </div>

                        <p class="text-muted mb-4">Clique no botão abaixo para baixar o relatório completo em formato CSV compatível com o Excel.</p>

                        <div class="d-grid gap-3">
                            <button @click="downloadCsv" class="btn btn-success btn-lg">
                                📥 Baixar Relatório (CSV)
                            </button>
                            <button @click="closeAdminModal" class="btn btn-outline-secondary">
                                Fechar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<style scoped>
.app-footer {
    background-color: #2d3748;
    color: #a0aec0;
    padding: 3rem 1.5rem 1.5rem;
    margin-top: 4rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.footer-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 2rem;
}

.footer-section {
    flex: 1;
    min-width: 280px;
}

.footer-title {
    color: #e2e8f0;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #4a5568;
    padding-bottom: 0.75rem;
}

.logo-wrapper {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.logo-placeholder {
    text-align: center;
}

.clickable-logo {
    cursor: pointer;
    transition: transform 0.1s ease;
    user-select: none;
}

.clickable-logo:active {
    transform: scale(0.95);
}

.logo-placeholder img {
    max-height: 80px;
    width: auto;
    max-width: 100%;
}

.logo-placeholder p {
    font-size: 0.8rem;
    margin-top: 0.5rem;
    color: #718096;
}

.dev-list {
    list-style: none;
    padding: 0;
    margin: 0;
    columns: 2;
    gap: 1rem;
}

.dev-list li {
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
}

.footer-copyright {
    max-width: 1200px;
    margin: 3rem auto 0;
    padding-top: 1.5rem;
    border-top: 1px solid #4a5568;
    text-align: center;
    font-size: 0.85rem;
    color: #718096;
}

/* Modal Administrativo */
.admin-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(6px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
}

.admin-modal-card {
    background-color: #ffffff;
    color: #1e293b;
    width: 90%;
    max-width: 460px;
    border-radius: 1rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    animation: modalScaleIn 0.2s ease-out;
}

@keyframes modalScaleIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.admin-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    background-color: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}

.admin-modal-header h3 {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0;
    color: #0f172a;
}

.btn-close-custom {
    background: none;
    border: none;
    font-size: 1.75rem;
    line-height: 1;
    color: #64748b;
    cursor: pointer;
}

.btn-close-custom:hover {
    color: #0f172a;
}

.admin-modal-body {
    padding: 1.75rem 1.5rem;
}

.pin-input {
    letter-spacing: 0.25rem;
    font-size: 1.5rem;
    font-weight: 700;
}

@media (max-width: 768px) {
    .footer-container {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .dev-list {
        columns: 1;
    }

    .logo-wrapper {
        justify-content: center;
        flex-direction: column;
        gap: 1rem;
    }

    .logo-placeholder img {
        max-height: 60px;
    }
}
</style>
