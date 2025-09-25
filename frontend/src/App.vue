<template>
  <div>
    <nav>
      <router-link to="/">Início</router-link> |
      <router-link to="/forms">Formulário de Consórcio</router-link>
    </nav>
    
    <router-view></router-view>
  </div>
</template>

<script setup>

</script>

<style>
nav {
  padding: 30px;
  text-align: center;
}
nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
}
nav a.router-link-exact-active {
  color: #42b983;
}
</style>  box-sizing: border-box;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}