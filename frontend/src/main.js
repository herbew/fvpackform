// main.js/ts
import {createApp} from 'vue'
import App from './App.vue'

// import "./assets/main.css"
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js"
import Paginate from "vuejs-paginate-next"

import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'


import router from './router'

import moment from "moment-timezone"
moment.tz.setDefault(process.env.VUE_APP_LOCAL_TIMEZONE)
moment.locale(process.env.VUE_APP_LOCAL_COUNTRY_ISO)

const app = createApp(App)

app.use(bootstrap)
app.use(Paginate)
app.component('VueDatePicker', VueDatePicker);
app.use(router)
app.use(moment)
app.mount('#app')

