import { createRouter, createWebHistory } from 'vue-router'
import SalesOrderItem from '../views/SalesOrderItem.vue'
import HelloWorld from '@/components/HelloWorld.vue'

const routes = [
    {
        path: '/',
        name: 'helloworld',
        component: HelloWorld
    },
    {
        path:'/order/',
        name:'sales_order',
        component:SalesOrderItem
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes:routes
})

export default router