<template>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <nav class="navbar navbar-light bg-light">
                    <div class="container-fluid">
                        <div class="col-md-3">
                            <VueDatePicker v-model="start_date" style="margin-right: 2px;"></VueDatePicker>
                        </div>
                        <div class="col-md-3">
                            <VueDatePicker v-model="end_date" style="margin-left: 2px;"></VueDatePicker>
                        </div>
                        <div class="col-md-6">
                            <form class="d-flex" style="margin-left: 5px;">
                                <input v-model="text_part" class="form-control me-2"  type="search" placeholder="Product Name .." aria-label="Search">
                                <button class="btn btn-outline-success" @click="submit" type="button">Search</button>
                            </form>
                        </div>
                    </div>
                    <div class="container-fluid">
                        <div class="col-md-12" style="text-align: left; margin-top: 15px; margin-bottom: -15px;">
                            <a class="navbar-brand"><label>Total Amount : {{ total_amount }}</label> </a>
                        </div>
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
                            <th scope="row" style="text-align: right;">{{ order_item.no }}</th>
                            <td style="text-align: left;">
                                {{ order_item.order_name }}<br>
                                <small>{{ order_item.product }}</small>
                            </td>
                            <td style="text-align: left;">
                                {{ order_item.company }}
                            </td>
                            <td style="text-align: left;">
                                {{ order_item.customer }}
                            </td>
                            <td v-if="order_item.order_date===null" style="text-align: right;">
                                <small v-if="created_at_is_desc===''">
                                    Ascending Ordered
                                </small>
                                <small v-else> Descending Ordered </small> &nbsp;
                                <div class="btn-group">
                                    <div class="btn-group dropup">
                                        <button type="button" @click="created_at_asc"
                                            class="btn btn-secondary dropdown-toggle" 
                                            aria-expanded="false"
                                            title="Ascending order by Order Date">
                                        </button>
                                    </div>
                                    <button 
                                        class="btn btn-light dropdown-toggle" 
                                        type="button" @click="created_at_desc" 
                                        aria-expanded="false"
                                        title="Descending order by Order Date">
                                    </button>
                                </div>
                            </td>
                            <td v-else style="text-align: left;">
                                {{ order_item.order_date }}
                            </td>
                            <td style="text-align: right;">
                                {{ order_item.delivered_amount }}
                            </td>
                            <td style="text-align: right;">
                                {{ order_item.total_amount }}
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

    import VueDatePicker from '@vuepic/vue-datepicker';
    import '@vuepic/vue-datepicker/dist/main.css'


    const URL_SALES_ORDER_ITEM  = 'http://192.168.0.144:8181/admin/api/sales/order/item/list/';
    
    export default {
        data(){
            return {
                pagination : null,
                page : 1,
                total_amount : 0,
                count : 0,
                links : null,
                order_items : [],
                created_at_is_desc:false,
                start_date : null,
                end_date : null
            }
        },
  
      async mounted(){
            this.clickCallback();
      },
  
      // Paginate
      components: {
        paginate: Paginate,VueDatePicker
      },
      methods: {
        created_at_asc(){
            if (this.reated_at_is_desc == ""){
                return
            }
            this.reated_at_is_desc = "";
            this.clickCallback(this.page);
        },
        created_at_desc(){
            if (this.reated_at_is_desc != ""){
                return
            }
            this.reated_at_is_desc = "True";
            this.clickCallback(this.page);
        },
        submit() {
            this.clickCallback(this.page);
        },
        clickCallback(pageNum){
            
            fetch(URL_SALES_ORDER_ITEM+"?page="+pageNum+"&part="+this.text_part+"&odesc="+this.reated_at_is_desc,
                {
                    method: "GET",
                    headers: {
                        "Content-type": "application/json;charset=UTF-8",
                        "Access-Control-Allow-Origin": "*"
                    }
                })
            .then(res => res.json())
            .then(data => {
                this.order_items = [
                    {
                        'no':null,
                        'order_name':null,
                        'product':null,
                        'company':null,
                        'customer':null,
                        'order_date':null,
                        'delivered_amount':null,
                        'total_amount':null
                    }
                ]

                data.data.forEach((item, index) => {
                    let d =  {
                        'no':item.no,
                        'order_name':item.row.order.order_name,
                        'product':item.row.product,
                        'company':item.row.order.customer.company.name,
                        'customer':item.row.order.customer.name,
                        'order_date':item.row.order.created_at_local_str,
                        'delivered_amount':item.row.total_delivered,
                        'total_amount':item.row.total_amount
                    }
                    this.order_items.push(d)
                    console.log(d)
                    console.log(index)
                })
                this.total_amount = data.total_amount;
                this.page = data.meta.pagination.page;
                this.pagination = {
                    'page':data.meta.pagination.page,
                    'pages':data.meta.pagination.pages,
                    'count':data.meta.pagination.count,
                    'per_page':data.meta.pagination.last,
                };
                this.created_at_is_desc = data.desc_order_created_at;
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
  
  
  
  
  
  
  
  
  
  
  
  
  TABLE SORTING
  https://github.com/bhaveshpatel200/vue3-datatable
  
  npm install @bhplugin/vue3-datatable --save
  