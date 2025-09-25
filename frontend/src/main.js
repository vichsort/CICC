import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import App from './App.vue';

import FormPage from './components/FormPage.vue';
import HomePage from './components/DashboardPage.vue'; 

const routes = [
  { path: '/', component: HomePage }, 
  { path: '/forms', component: FormPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');