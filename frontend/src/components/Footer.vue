<script setup>
import { ref } from 'vue';


const developers = ref([
    'Gabriel Moura Jappe',
    'Gustavo Schwitzki Peretti',
    'Vitor Marcelo Mignoni',
    'Heitor Scalco Neto'
]);

const currentYear = new Date().getFullYear();
</script>

<template>
    <footer class="app-footer">
        <div class="footer-container">
            <div class="footer-section logos-section">
                <h4 class="footer-title">Realização</h4>
                <div class="logo-wrapper">
                    <div class="logo-placeholder">
                        <img src="../assets/ita.png">
                        <p>Consórcio Itá</p>
                    </div>

                    <div class="logo-placeholder">
                        <img src="../assets/ifc_white.png">
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

.logo-instruction {
    font-size: 0.75rem;
    color: #718096;
    margin-top: 1.5rem;
    font-style: italic;
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
