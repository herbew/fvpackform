// main.js/ts
import {createApp} from 'vue'
import App from './App.vue'

// import "./assets/main.css"
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js"
import Paginate from "vuejs-paginate-next";

import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'


const app = createApp(App)
app.use(bootstrap)
app.use(Paginate)
app.component('VueDatePicker', VueDatePicker);
app.mount('#app')

