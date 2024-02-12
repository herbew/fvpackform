<template>
    <div>
        <h1>Sales Order Item</h1>
        <div v-for="order_item in order_items.data" :key="order_item" class="sales_order_item">
            <h3>{{ order_item.id }} - {{ order_item.order }}</h3>
        </div>
    </div>
</template>
<script>
    export default{
        data(){
            return {
                order_items : []
            }
        },
        mounted(){
            fetch('http://192.168.0.144:8181/admin/api/sales/order/item/list/',
                {
                    method: "GET",
                    headers: {
                        "Content-type": "application/json;charset=UTF-8",
                        "Access-Control-Allow-Origin": "*"
                    }
                })
            .then(res => res.json())
            .then(data => this.order_items = data)
            .catch(err => console.log(err.message))
        }
    }
</script>
