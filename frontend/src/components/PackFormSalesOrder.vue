<template>
  <div class="PackFormSalesOrderMessage">
    <h1>{{ msg }}</h1>
  </div>
  <div id="app">{{ info }}</div>
</template>

<script>
export default {
  name: "PackFormSalesOrder",
  props: {
    msg: String,
    info: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
