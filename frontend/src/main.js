// main.js/ts
import {createApp} from 'vue'
import App from './App.vue'

// import "./assets/main.css"
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js"
import Paginate from "vuejs-paginate-next";

const app = createApp(App)
app.use(bootstrap)
app.use(Paginate)
app.mount('#app')

