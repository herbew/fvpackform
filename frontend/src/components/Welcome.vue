<template>
  <div class="hello">
    <img alt="Vue logo" src="../assets/logo.png">
    <div class="container">
      <tr>
        <div class="col-12">
          <h1>Welcome to Sales Order Service</h1>
        </div>
        
      </tr>
      <tr>
          <table>
            <div class="col-12">
              <td class="col-4"></td>
              <td class="col-6" style="text-align: left;">
                <p>
                  This service for helping Staff to check their Customer.<br>
                  Follow the SOP as:<br>
                  - Enter the <b>Product Name</b> then klik Search button.<br>
                  - Klik <b>Start date</b> and or <b>End date</b> for filtering created date of order.<br>      
                  - Klik the pagination button, if you will see the other page.<br>
                  - Don't forget, you enable <b>order</b> the data by a created date or order
                </p>
                <p>
                  Best Regard,<br>
                  Heribertus Rustyawan
                </p>
              </td>
              <td class="col-2"></td>
          </div>
        </table>
      </tr>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
}
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