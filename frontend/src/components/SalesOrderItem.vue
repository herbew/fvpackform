<template>
  <div class="container">
      <div class="card">
          <div class="card-header">
              <nav class="navbar navbar-light bg-light">
                  <div class="container-fluid">
                      <a class="navbar-brand"><label>Total Amount : {{ total_amount }}</label> </a>
                      <form class="d-flex">
                          <input v-model="text_part" class="form-control me-2"  type="search" placeholder="Product Name .." aria-label="Search">
                          <button class="btn btn-outline-success" @click="submit" type="button">Search</button>
                      </form>
                  </div>
              </nav>
          </div>
          <div class="card-body">
              <table class="table table-striped">
                  <thead>
                      <tr>
                      <th scope="col">#</th>
                      <th scope="col">Order Name</th>
                      <th scope="col">Company Customer</th>
                      <th scope="col">Customer Name</th>
                      <th scope="col">Order Date</th>
                      <th scope="col">Delivered Amount</th>
                      <th scope="col">Total Amount</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="order_item in order_items" :key="order_item">
                          <th scope="row" style="text-align: right;">{{ order_item.no }}.</th>
                          <td style="text-align: left;">
                              {{ order_item.row.order.order_name }}<br>
                              <small>{{ order_item.row.product }}</small>
                          </td>
                          <td style="text-align: left;">
                              {{ order_item.row.order.customer.company.name }}
                          </td>
                          <td style="text-align: left;">
                              {{ order_item.row.order.customer.name }}
                          </td>
                          <td style="text-align: left;">
                              {{ order_item.row.order.created_at_local }}
                          </td>
                          <td style="text-align: right;">
                              {{ order_item.row.total_delivered }}
                          </td>
                          <td style="text-align: right;">
                              {{ order_item.row.total_amount }}
                          </td>
                      </tr>
                  </tbody>
              </table>
              
          </div>
          <div class="col-md-12 card-footer text-muted">
                <td class="col-md-6" style="text-align: left;">
                    <label>Total items : <font v-if="pagination">{{ pagination.count }}</font></label>
                </td>
                <td class="col-md-6" style="text-align: right;">
                    <div v-if="count === 0">Please insert the Product Name!</div>
                    <div v-else>
                        <paginate
                        :page-count="pagination.pages"
                        :page-range="pagination.per_page"
                        :margin-pages="pagination.pages"
                        :click-handler="clickCallback"
                        :prev-text="'Prev'"
                        :next-text="'Next'"
                        :container-class="'pagination'"
                        :page-class="'page-item'"
                        >
                        </paginate>
                    </div>
                </td>
          </div>
      </div>       
  </div>
</template>

<script>
  // Pagination
  import Paginate from 'vuejs-paginate-next';

  const URL_SALES_ORDER_ITEM  = 'http://192.168.0.144:8181/admin/api/sales/order/item/list/';
  
  export default {
      data(){
          return {
              pagination : null,
              page : 1,
              total_amount : 0,
              count : 0,
              links : null,
              order_items : []
          }
      },

    async mounted(){
          this.clickCallback();
    },

    // Paginate
    components: {
      paginate: Paginate,
    },
    methods: {
      
      submit() {
          this.clickCallback(this.page);
      },
      clickCallback(pageNum){
          
          fetch(URL_SALES_ORDER_ITEM+"?page="+pageNum+"&part="+this.text_part,
              {
                  method: "GET",
                  headers: {
                      "Content-type": "application/json;charset=UTF-8",
                      "Access-Control-Allow-Origin": "*"
                  }
              })
          .then(res => res.json())
          .then(data => {
              this.order_items = data.data;
              this.total_amount = data.total_amount;
              this.page = data.meta.pagination.page;
              this.pagination = {
                  'page':data.meta.pagination.page,
                  'pages':data.meta.pagination.pages,
                  'count':data.meta.pagination.count,
                  'per_page':data.meta.pagination.last,
              };
              this.links = {
                  'first':data.links.first,
                  'next':data.links.next,
                  'prev':data.links.prev,
                  'last':data.links.last,
              };
              this.count = data.meta.pagination.count;
          })
          .catch(err => console.log(err.message))
          console.log(URL_SALES_ORDER_ITEM+"?page="+pageNum+"&part="+this.text_part);
          console.log(this.order_items)
          console.log(this.text_part)
      }
    },
    
  };
</script>

<style lang="css">
  /* Adopt bootstrap pagination stylesheet. */
  @import "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css";

  /* Write your own CSS for pagination */
  .pagination {
  }
  .page-item {
  }
</style>