<template>
    <div class="container">
      <nav>
          <router-link to="/">Home</router-link> &nbsp;
          <router-link to="/orders">Sales Order</router-link>
      </nav>
      <router-view></router-view>
    </div>
</template>

<script>
  export default {
    name: 'App',
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>