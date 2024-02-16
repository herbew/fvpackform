<template>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <nav class="navbar navbar-light bg-light">
                    <div class="container-fluid">
                        <div class="col-md-3">
                            <VueDatePicker 
                                v-model="start_date" 
                                @open="start_date_init"
                                style="margin-right: 2px;">
                            </VueDatePicker>
                        </div>
                        <div class="col-md-3">
                            <VueDatePicker 
                                v-model="end_date" 
                                @open="end_date_init"
                                style="margin-left: 2px;">
                            </VueDatePicker>
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
                                <small v-if="created_at_is_desc===''" class="text-success">
                                    Ascending Ordered
                                </small>
                                <small v-else class="text-danger"> Descending Ordered </small> &nbsp;
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
            <div class="col-12 card-footer text-muted">
                  <td class="col-8" style="text-align: left;">
                      <label class="text-primary">
                            Total items : <font v-if="pagination" >{{ pagination.count }}</font>, <small class="text-info"> {{ today_date }}</small>
                      </label>
                  </td>
                  <td  style="text-align: right;">
                      <div v-if="count === 0">
                        <label v-if="err_api" class="text-danger">{{ err_api }}</label>
                        <lable v-else>Please insert the Product Name!</lable>
                      </div>
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
    
    // DatePicker
    import VueDatePicker from '@vuepic/vue-datepicker';
    import '@vuepic/vue-datepicker/dist/main.css'

    // moment for datetime processing
    import moment from 'moment'

    // default url api for env
    const URL_SALES_ORDER_ITEM  = process.env.VUE_APP_APIURL_SALES_ORDER_ITEM; 
    
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
                end_date : null,
                today_date: moment().local(true).format('MMMM Do YYYY, h:mm:ss a'),
                text_part: null,
                err_api: null        
            }
        },
  
      async mounted(){
            // mounted the raw data
            this.clickCallback();
      },
  
      // export components : Paginate, VueDatePicker
      components: {
        paginate: Paginate, VueDatePicker
      },

      methods: {
        start_date_init(){
            // Intialize the start_date DatePicker, as local date(AEDT base env)
            this.start_date = moment().local(true)
        },

        end_date_init(){
            // Intialize the end_date DatePicker, as local date(AEDT base env)
            this.end_date = moment().local(true)
        },

        created_at_asc(){
            // Ordering ASC base created_at field
            if (this.reated_at_is_desc == ""){
                return
            }
            this.reated_at_is_desc = "";
            this.clickCallback(this.page);
        },

        created_at_desc(){
            // Ordering DESC base created_at field
            if (this.reated_at_is_desc != ""){
                return
            }
            this.reated_at_is_desc = "True";
            this.clickCallback(this.page);
        },

        submit() {
            // Submit, Check if any filter start_date or end_date
            if(this.start_date && this.end_date){
                if(this.start_date > this.end_date){
                    alert('The start date must be less than the end date!');
                    this.start_date = null;
                    this.end_date = null;
                    return
                }
            }
            // Call fetch url data
            this.pagination = {
                    'page':1,
                    'pages':1,
                    'count':0,
                    'per_page':0,
                };
            this.page = 1
            this.clickCallback(this.page);
        },
        clickCallback(pageNum){
            // Initial url
            let so_url = URL_SALES_ORDER_ITEM+"?page="+pageNum;
            
            // Add the param filter 'odesc' for DESC order
            if(this.reated_at_is_desc){
                so_url = so_url+"&odesc="+this.reated_at_is_desc
            }

            // Add the param filter 'part' 
            if(this.text_part){
                so_url = so_url+"&part="+this.text_part
            }
            
            // Add the param filter 'sdt', start date created_at
            if (this.start_date){
                let str_start_date = moment(this.start_date).format("YYYY-MM-DDThh:mm:ss") + "Z"
                so_url = so_url+"&sdt="+str_start_date
            }
            
            // Add the param filter 'edt', end date created_at
            if (this.end_date){
                let str_end_date = moment(this.end_date).format("YYYY-MM-DDThh:mm:ss") + "Z"
                so_url = so_url+"&edt="+str_end_date
            }
            console.log(so_url)
            

            fetch(so_url,
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

                data.data.forEach((item) => {
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
                    //console.log(d)
                    //console.log(index)
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
                this.err_api = null;
            })
            .catch(err => {
                this.count = 0;
                this.order_items = [];
                this.err_api = 'Any Error with REST API Item Order';
                this.total_amount = 0;
                this.page = 0;
                console.log(err.message);
            }
            )
            //console.log(URL_SALES_ORDER_ITEM+"?page="+pageNum+"&part="+this.text_part);
            //console.log(this.order_items)
            //console.log(this.text_part)
        }
      },
      
    };
  </script>
  
  
  
  
  
  
  
  
  
  
  
  
  
  TABLE SORTING
  https://github.com/bhaveshpatel200/vue3-datatable
  
  npm install @bhplugin/vue3-datatable --save
  