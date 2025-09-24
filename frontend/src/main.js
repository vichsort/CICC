import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import App from './App.vue';

import ConsorcioltaForm from './components/forms.vue';
import HomePage from './components/DashboardPage.vue'; 

const routes = [
  { path: '/', component: HomePage }, 
  { path: '/consorcio', component: ConsorcioltaForm }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 4. Use o router e monte a aplicação
const app = createApp(App);
app.use(router);
app.mount('#app');