new = Vue({el: '#app', data (){return {info:null}}}, mounted ({axios
.get('https://api.coindesk.com/v1/bpi/currentprice.json').then(response =>
(this.info = response))}))
<template>
  <!--
  <img alt="Vue logo" src="./assets/logo.png" />
  -->
  <PackFormSalesOrderMessage msg="Welcome to PackForm Sales Order App" />
  <PackFormSalesOrderApi info="{{}}" />
</template>

<script>
import PackFormSalesOrderMessage from "./components/PackFormSalesOrder.vue";
import PackFormSalesOrderApi from "./components/PackFormSalesOrder.vue";

export default {
  name: "App",
  components: {
    PackFormSalesOrderMessage,
    PackFormSalesOrderApi,
  },
};
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
