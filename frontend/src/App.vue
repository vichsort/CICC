<template>
  <div>
    <nav>
      <img src="./assets/ifc.png">
      <div class="links">
        <router-link to="/">Início</router-link>
        <router-link to="/forms">Formulário de Consórcio</router-link>
      </div>
      <img src="./assets/ita.png">
    </nav>
    
    <router-view></router-view>
  </div>
</template>

<style>
  body {
    overflow-x: hidden;
  }

  nav {
    padding: 20px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    text-align: center;
  }

  nav img {
    height: 80px;
  }

  nav img:first-child {
    justify-self: start;
  }

  nav .links {
    display: flex;
    justify-content: center;
    justify-self: center;
  }

  nav img:last-child {
    justify-self: end;
  }

  nav a {
    font-weight: bold;
    color: #21314a;
    margin: 0 10px;
    text-decoration: none;
    font-size: 1.25em;
  }

  nav a.router-link-exact-active {
    color: #0d6efd;
  }

  @media (max-width: 1024px) {
    nav .links {
      flex-direction: column;
    }
  }

  @media (max-width: 820px) {
    nav img {
      height: 65px;
    }

    nav a {
      font-size: 1em;
    }
  }

</style>