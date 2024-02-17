import { createRouter, createWebHistory } from 'vue-router'
import SalesOrderItem from '../views/SalesOrderItem.vue'
import Welcome from '@/components/Welcome.vue'

const routes = [
    {
        path: '/',
        name: 'welcome',
        component: Welcome
    },
    {
        path:'/orders',
        name:'sales_order',
        component:SalesOrderItem
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes:routes
})

export default router